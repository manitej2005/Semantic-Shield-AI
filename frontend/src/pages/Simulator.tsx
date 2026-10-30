import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Crosshair,
  ShieldAlert,
  Sparkles,
  ArrowRight,
  Eye,
  Search,
  Filter,
  CheckCircle2,
  AlertTriangle,
  Mail,
  Link as LinkIcon,
  X,
  UserCheck,
  Flag,
  AlertOctagon,
  ShieldCheck,
  RotateCcw,
  Check,
} from 'lucide-react';
import { DEMO_DATASET, DemoSample } from '../data/demoDataset';
import { DashboardContext } from '../contexts/DashboardContext';

export const SimulatorPage: React.FC = () => {
  const navigate = useNavigate();
  const context = useContext(DashboardContext);

  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Simulation Drawer & Interactive State
  const [activeSimulationSample, setActiveSimulationSample] = useState<DemoSample | null>(null);
  const [userDecisions, setUserDecisions] = useState({
    opened: false,
    clickedLink: false,
    verifiedSender: false,
    reportedPhishing: false,
    ignored: false,
  });
  const [behavioralAssessment, setBehavioralAssessment] = useState<any | null>(null);

  // Live Simulation State
  const [selectedProfile, setSelectedProfile] = useState<string>('trusting');
  const [isLiveSimulating, setIsLiveSimulating] = useState<boolean>(false);
  const [liveReasoning, setLiveReasoning] = useState<string>('');
  const [liveResult, setLiveResult] = useState<any | null>(null);

  const profileRoleMap: Record<string, string> = {
    trusting: 'HR Manager',
    security_conscious: 'Senior Developer',
    overwhelmed: 'Finance Manager',
    executive: 'VP of Operations',
  };

  const filteredSamples = DEMO_DATASET.filter((sample) => {
    const matchesCategory = selectedCategory === 'ALL' || sample.category === selectedCategory;
    const matchesDifficulty = selectedDifficulty === 'ALL' || sample.difficulty === selectedDifficulty;
    const matchesSearch =
      searchQuery === '' ||
      sample.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sample.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sample.id.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesDifficulty && matchesSearch;
  });

  const startSimulation = (sample: DemoSample) => {
    setActiveSimulationSample(sample);
    setLiveReasoning('');
    setLiveResult(null);
    setUserDecisions({
      opened: true, // User opens scenario to view inbox content
      clickedLink: false,
      verifiedSender: false,
      reportedPhishing: false,
      ignored: false,
    });
    setBehavioralAssessment(null);
  };

  const runLiveSimulation = async (profileName?: string) => {
    if (!activeSimulationSample) return;
    const targetProf = profileName || selectedProfile;
    setSelectedProfile(targetProf);
    setIsLiveSimulating(true);
    setLiveReasoning('');
    setLiveResult(null);

    try {
      const payload = {
        scenario: activeSimulationSample.title,
        employee_role: profileRoleMap[targetProf] || 'Employee',
        behavior_profile: targetProf,
        email_subject: activeSimulationSample.subject || activeSimulationSample.title,
        email_body: activeSimulationSample.rawContent,
      };

      const res = await fetch('http://127.0.0.1:8000/api/v1/phishing-simulation/simulate?stream=true', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok || !res.body) throw new Error('Simulation API stream failed');

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event = JSON.parse(line.slice(6));
              if (event.type === 'reasoning') {
                setLiveReasoning((prev) => prev + event.content);
              } else if (event.type === 'result') {
                setLiveResult(event.data);
              }
            } catch (e) {
              // ignore partial json
            }
          }
        }
      }
    } catch (err) {
      console.error('Live simulation error:', err);
    } finally {
      setIsLiveSimulating(false);
    }
  };

  const recordChoice = (action: 'ignore' | 'report' | 'click' | 'verify') => {
    const updated = { ...userDecisions };
    if (action === 'ignore') {
      updated.ignored = true;
    } else if (action === 'report') {
      updated.reportedPhishing = true;
    } else if (action === 'click') {
      updated.clickedLink = true;
    } else if (action === 'verify') {
      updated.verifiedSender = true;
    }

    setUserDecisions(updated);

    // Evaluate Behavioral Assessment
    if (!activeSimulationSample) return;
    const isPhishing = activeSimulationSample.expectedClassification !== 'Safe';

    if (action === 'click' && isPhishing) {
      setBehavioralAssessment({
        riskLevel: 'Critical',
        summary: 'High Risk Action: Clicked unverified link in suspicious payload.',
        recommendation:
          'Always inspect destination URLs and perform sender domain verification before interacting with links.',
      });
    } else if (action === 'report' && isPhishing) {
      setBehavioralAssessment({
        riskLevel: 'Low',
        summary: 'Exemplary Defensive Behavior: Recognized social engineering indicators and reported payload.',
        recommendation: 'Excellent work! Prompt reporting allows SOC teams to block attack campaigns network-wide.',
      });
    } else if (action === 'verify') {
      setBehavioralAssessment({
        riskLevel: updated.clickedLink ? 'Medium' : 'Low',
        summary: 'Proactive Security Check: Inspected sender headers and technical origin domain.',
        recommendation:
          updated.clickedLink
            ? 'Sender checked, but unverified links were clicked. Avoid clicking links prior to SOC confirmation.'
            : 'Good vigilance. Verification confirmed sender domain anomalies.',
      });
    } else if (action === 'ignore') {
      setBehavioralAssessment({
        riskLevel: isPhishing ? 'Medium' : 'Low',
        summary: 'Passive Action: Suspicious email ignored.',
        recommendation:
          'While ignoring prevents credentials from being compromised, reporting suspicious emails protects peers.',
      });
    }
  };

  const handleAnalyzeWithDefensiveAI = (sample: DemoSample) => {
    if (context?.setTransferredSample) {
      context.setTransferredSample(sample);
    }
    navigate('/dashboard');
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-amber-950/40 border border-slate-800 shadow-xl">
        <div>
          <div className="flex items-center space-x-2 text-amber-400 text-xs font-mono font-semibold uppercase tracking-wider mb-1">
            <Sparkles className="w-4 h-4" />
            <span>Offensive AI Simulation Sandbox</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <Crosshair className="w-7 h-7 text-amber-400" />
            <span>Phishing Simulation & Behavioral Threat Analysis</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl">
            Educational controlled simulation environment. Test interactive employee response behaviors against real attack scenarios and seamlessly analyze payloads with Defensive AI.
          </p>
        </div>

        <div className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-amber-950/60 border border-amber-500/30 text-amber-300 text-xs font-mono shrink-0">
          <ShieldAlert className="w-4 h-4 text-amber-400" />
          <span>Educational Simulation Engine</span>
        </div>
      </div>

      {/* Filters & Search Control Bar */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between p-4 rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-md">
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search attack scenarios..."
            className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 transition-colors"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
          {/* Category Filter */}
          <div className="flex items-center space-x-1 text-xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-400">Category:</span>
          </div>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Attack Categories</option>
            <option value="Credential Harvest">Credential Harvest</option>
            <option value="Banking Scam">Banking Scam</option>
            <option value="HR / Payroll Scam">HR / Payroll Scam</option>
            <option value="Delivery Scam">Delivery Scam</option>
            <option value="M365 Impersonation">M365 Impersonation</option>
            <option value="MFA Bypass">MFA Bypass</option>
            <option value="Legitimate">Legitimate</option>
          </select>

          {/* Difficulty Filter */}
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Difficulties</option>
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
        </div>
      </div>

      {/* Simulation Scenarios Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredSamples.map((sample) => (
          <div
            key={sample.id}
            className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 hover:border-slate-700 transition-all flex flex-col justify-between space-y-4 group"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <Mail className="w-4 h-4 text-cyan-400" />
                  <span className="text-xs font-mono font-bold text-slate-400 uppercase">
                    {sample.id}
                  </span>
                </div>

                <div className="flex items-center space-x-2">
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                      sample.expectedClassification === 'Critical'
                        ? 'bg-rose-950/80 text-rose-400 border border-rose-500/30'
                        : sample.expectedClassification === 'Phishing'
                        ? 'bg-amber-950/80 text-amber-400 border border-amber-500/30'
                        : 'bg-emerald-950/80 text-emerald-400 border border-emerald-500/30'
                    }`}
                  >
                    {sample.expectedClassification} ({sample.expectedRiskScore})
                  </span>
                  <span className="px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 text-[10px] font-mono">
                    {sample.difficulty}
                  </span>
                </div>
              </div>

              <div>
                <h3 className="text-base font-bold text-white group-hover:text-amber-300 transition-colors">
                  {sample.title}
                </h3>
                <p className="text-xs text-slate-400 mt-1 line-clamp-2">{sample.description}</p>
              </div>

              {/* Key indicators tags */}
              <div className="flex flex-wrap gap-1.5 pt-1">
                {sample.keyIndicators.slice(0, 3).map((ind, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-0.5 rounded-md bg-slate-950 text-slate-400 text-[10px] border border-slate-800/80"
                  >
                    {ind}
                  </span>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center justify-between gap-3 pt-3 border-t border-slate-800/60">
              <button
                onClick={() => startSimulation(sample)}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 text-xs font-semibold transition-colors"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Interactive Simulation</span>
              </button>

              <button
                onClick={() => handleAnalyzeWithDefensiveAI(sample)}
                className="flex items-center space-x-1.5 px-4 py-1.5 rounded-xl bg-gradient-to-r from-cyan-600 to-emerald-600 hover:from-cyan-500 hover:to-emerald-500 text-white text-xs font-semibold shadow-lg shadow-cyan-950/40 transition-all"
              >
                <span>Analyze with Defensive AI</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Interactive Simulation Drawer / Modal */}
      {activeSimulationSample && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md">
          <div className="w-full max-w-3xl rounded-2xl border border-slate-800 bg-slate-900 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-950/80">
              <div className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-amber-400" />
                <div>
                  <h3 className="text-base font-bold text-white">
                    Phishing Simulation: {activeSimulationSample.title}
                  </h3>
                  <p className="text-xs text-slate-400">
                    ID: {activeSimulationSample.id} | Category: {activeSimulationSample.category}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setActiveSimulationSample(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Simulated Email Client Inbox View */}
            <div className="p-6 space-y-5 overflow-y-auto">
              <div className="rounded-xl border border-slate-800 bg-slate-950 p-4 space-y-3 font-sans">
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 text-xs">
                  <div className="space-y-1">
                    <p className="text-slate-300 font-bold">
                      From: <span className="text-cyan-400 font-mono">{activeSimulationSample.sender || 'Unknown Sender'}</span>
                    </p>
                    <p className="text-white font-semibold">Subject: {activeSimulationSample.subject}</p>
                  </div>
                  <span className="px-2.5 py-1 rounded-md bg-slate-900 text-slate-400 text-[10px] font-mono border border-slate-800">
                    Simulated Inbox
                  </span>
                </div>

                <div className="text-xs text-slate-300 font-mono whitespace-pre-wrap leading-relaxed p-3 rounded-lg bg-slate-900/50 border border-slate-800">
                  {activeSimulationSample.rawContent}
                </div>
              </div>

              {/* Live Gemini Simulation Trigger Controls */}
              <div className="p-4 rounded-xl border border-slate-800 bg-slate-950/90 space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-2.5">
                  <div>
                    <p className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Live Gemini Agent Behavioral Simulation</span>
                    </p>
                    <p className="text-[11px] text-slate-400 mt-0.5">Select an employee behavioral profile to test against live LLM reasoning.</p>
                  </div>

                  <div className="flex items-center space-x-1">
                    {[
                      { key: 'trusting', label: 'Trusting (HR)' },
                      { key: 'security_conscious', label: 'Security-Conscious (Dev)' },
                      { key: 'overwhelmed', label: 'Overwhelmed (Finance)' },
                      { key: 'executive', label: 'Executive (VP)' },
                    ].map((p) => (
                      <button
                        key={p.key}
                        onClick={() => {
                          setSelectedProfile(p.key);
                          runLiveSimulation(p.key);
                        }}
                        disabled={isLiveSimulating}
                        className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition-all ${
                          selectedProfile === p.key
                            ? 'bg-amber-500/20 text-amber-300 border border-amber-500/50'
                            : 'bg-slate-900 text-slate-400 border border-slate-800 hover:text-white'
                        }`}
                      >
                        {p.label}
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  onClick={() => runLiveSimulation()}
                  disabled={isLiveSimulating}
                  className="w-full py-2.5 rounded-xl bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-white font-bold text-xs shadow-md transition-all disabled:opacity-50 flex items-center justify-center space-x-2"
                >
                  <Sparkles className={`w-4 h-4 ${isLiveSimulating ? 'animate-spin' : ''}`} />
                  <span>{isLiveSimulating ? 'Streaming Gemini Reasoning...' : `Run Simulation as [${profileRoleMap[selectedProfile]}]`}</span>
                </button>
              </div>

              {/* Streamed Gemini Agent Reasoning Output */}
              {(liveReasoning || isLiveSimulating) && (
                <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 space-y-2.5 animate-in fade-in duration-200">
                  <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
                    <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 animate-pulse" />
                      <span>Live Streamed Gemini Agent Reasoning</span>
                    </span>
                    {isLiveSimulating && (
                      <span className="text-[10px] font-mono text-cyan-400 animate-pulse">Streaming Response...</span>
                    )}
                  </div>
                  <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-200 whitespace-pre-wrap max-h-56 overflow-y-auto leading-relaxed">
                    {liveReasoning || 'Initializing Gemini LLM stream...'}
                  </div>
                </div>
              )}

              {/* Final Simulation Result Card */}
              {liveResult && (
                <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 space-y-3 animate-in fade-in duration-200">
                  <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                    <div>
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Agent Decision Result</span>
                      <span
                        className={`text-lg font-extrabold tracking-wide uppercase px-3 py-0.5 rounded-lg inline-block mt-0.5 ${
                          liveResult.agent_decision === 'VULNERABLE'
                            ? 'bg-rose-950 text-rose-400 border border-rose-500/40'
                            : 'bg-emerald-950 text-emerald-400 border border-emerald-500/40'
                        }`}
                      >
                        [{liveResult.agent_decision}]
                      </span>
                    </div>

                    <div className="text-right">
                      <span className="text-[10px] font-bold text-slate-400 uppercase block">Composite Risk Score</span>
                      <span
                        className={`text-2xl font-black ${
                          liveResult.risk_score >= 70
                            ? 'text-rose-400'
                            : liveResult.risk_score >= 40
                            ? 'text-amber-400'
                            : 'text-emerald-400'
                        }`}
                      >
                        {liveResult.risk_score}/100
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                    <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                      <span className="text-[10px] text-slate-400 uppercase block">Threat Category</span>
                      <strong className="text-slate-200 capitalize">{liveResult.threat_category || 'phishing'}</strong>
                    </div>

                    <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                      <span className="text-[10px] text-slate-400 uppercase block">Severity Level</span>
                      <strong
                        className={
                          liveResult.threat_severity === 'DANGEROUS'
                            ? 'text-rose-400'
                            : liveResult.threat_severity === 'SUSPICIOUS'
                            ? 'text-amber-400'
                            : 'text-emerald-400'
                        }
                      >
                        {liveResult.threat_severity}
                      </strong>
                    </div>

                    <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                      <span className="text-[10px] text-slate-400 uppercase block">Confidence Score</span>
                      <strong className="text-cyan-400">{liveResult.confidence_score}%</strong>
                    </div>

                    <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                      <span className="text-[10px] text-slate-400 uppercase block">Duration</span>
                      <strong className="text-slate-200">{liveResult.duration_seconds}s</strong>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-slate-800 bg-slate-950/80 flex items-center justify-between">
              <span className="text-xs text-slate-400">
                Technique: <strong className="text-white">{activeSimulationSample.techniqueExplanation}</strong>
              </span>
              <button
                onClick={() => {
                  const s = activeSimulationSample;
                  setActiveSimulationSample(null);
                  handleAnalyzeWithDefensiveAI(s);
                }}
                className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold transition-all shadow-md shadow-cyan-950/50"
              >
                <span>Analyze with Defensive AI</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SimulatorPage;
