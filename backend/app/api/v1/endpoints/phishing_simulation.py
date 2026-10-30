"""
FastAPI REST API Endpoints for Phishing Simulation Engine.
Exposes POST /api/v1/phishing-simulation/simulate with real-time reasoning streaming support.
"""

import json
import logging
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse

from app.schemas.phishing_simulation import (
    PhishingSimulationRequest,
    PhishingSimulationResponse,
)
from app.services.phishing_simulation.engine import phishing_simulation_engine
from app.services.phishing_simulation.system_prompts import PROMPTS

logger = logging.getLogger("app.api.v1.endpoints.phishing_simulation")

router = APIRouter()


@router.post(
    "/simulate",
    summary="Run Phishing Simulation Test",
    description="Simulates how an employee with a specific behavioral profile responds to a phishing email attack vector.",
    response_model=PhishingSimulationResponse,
)
async def simulate_phishing_attack(payload: PhishingSimulationRequest, stream: bool = False):
    """
    Executes a Phishing Simulation run.
    Supports both standard JSON response and real-time streaming chunk response when stream=true.
    """
    # 1. Validation: Check required fields
    if not payload.scenario or not payload.scenario.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'scenario' cannot be empty."
        )

    if not payload.employee_role or not payload.employee_role.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'employee_role' cannot be empty."
        )

    if not payload.email_subject or not payload.email_subject.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'email_subject' cannot be empty."
        )

    if not payload.email_body or not payload.email_body.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'email_body' cannot be empty."
        )

    # Validate behavioral profile
    normalized_profile = (payload.behavior_profile or "").strip().lower()
    if normalized_profile not in PROMPTS:
        valid_options = ", ".join(PROMPTS.keys())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid behavior_profile '{payload.behavior_profile}'. Choose from: {valid_options}"
        )

    try:
        sim_id, now_iso, system_prompt, user_message, start_time, stream_gen = (
            await phishing_simulation_engine.execute_simulation(payload)
        )

        if stream:
            # Stream response as Server-Sent Events / JSON lines
            async def event_stream() -> AsyncGenerator[str, None]:
                accumulated_text = []
                async for chunk in stream_gen():
                    accumulated_text.append(chunk)
                    chunk_event = {"type": "reasoning", "content": chunk}
                    yield f"data: {json.dumps(chunk_event)}\n\n"

                full_text = "".join(accumulated_text)
                final_response = await phishing_simulation_engine.finalize_simulation(
                    sim_id=sim_id,
                    now_iso=now_iso,
                    request=payload,
                    full_reasoning_text=full_text,
                    start_time=start_time,
                )

                final_event = {"type": "result", "data": final_response.dict()}
                yield f"data: {json.dumps(final_event)}\n\n"

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        else:
            # Non-streaming standard JSON response
            accumulated_text = []
            async for chunk in stream_gen():
                accumulated_text.append(chunk)

            full_text = "".join(accumulated_text)
            final_response = await phishing_simulation_engine.finalize_simulation(
                sim_id=sim_id,
                now_iso=now_iso,
                request=payload,
                full_reasoning_text=full_text,
                start_time=start_time,
            )
            return final_response

    except ValueError as ve:
        logger.warning(f"[Simulation API] Validation error: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as exc:
        logger.error(f"[Simulation API] Execution error: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Phishing simulation execution failed: {str(exc)}"
        )
