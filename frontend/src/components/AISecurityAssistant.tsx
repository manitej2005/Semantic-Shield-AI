import React, { useState, useContext } from 'react';
import { Bot, X, Send, Sparkles, AlertTriangle, ShieldCheck } from 'lucide-react';
import { DashboardContext } from '../contexts/DashboardContext';

interface ChatMessage {
  id: string;
  sender: 'ai' | 'user';
  text: string;
  timestamp: string;
}

export const AISecurityAssistant: React.FC = () => {
  const context = useContext(DashboardContext);
  const latestScanResult = context?.latestScanResult;

  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [inputText, setInputText] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'msg-1',
      sender: 'ai',
      text: 'Hello! I am your SemanticShield AI Security Assistant. Ask me anything about scan results, phishing indicators, or safe browsing advice. You can also ask "Explain my latest scan".',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);

  const handleSend = (textToSend?: string) => {
    const text = textToSend || inputText;
    if (!text.trim()) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    const query = text.toLowerCase();
    if (!textToSend) setInputText('');

    // Generate context-aware security advice answer
    setTimeout(() => {
      let replyText =
        'I am analyzing your security query against established threat indicators. Always verify email sender headers and avoid clicking unverified links.';

      if (query.includes('latest') || query.includes('last scan') || query.includes('explain')) {
        if (latestScanResult) {
          replyText = `Regarding your latest scan "${latestScanResult.title}" (ID: ${latestScanResult.id}): It was classified as ${latestScanResult.classification.toUpperCase()} with a Risk Score of ${latestScanResult.riskScore}/100. ${latestScanResult.aiExplanation} Flagged indicators include: ${latestScanResult.keyIndicators.join(', ')}.`;
        } else {
          replyText =
            'No scan has been executed yet in this session. Run a scan in the Defensive Scanner or select a sample from the Simulation Lab to inspect live telemetry.';
        }
      } else if (query.includes('spf') || query.includes('dkim') || query.includes('dmarc')) {
        replyText =
          'SPF (Sender Policy Framework), DKIM, and DMARC are email authentication protocols. If any of these checks fail, it indicates that the sender address may be forged or spoofed.';
      } else if (query.includes('spoof') || query.includes('display name')) {
        replyText =
          'Display Name Spoofing occurs when an attacker sets their email display name to mimic an executive or trusted brand (e.g. "Microsoft Team") while using an external email address.';
      } else if (query.includes('qr') || query.includes('quishing')) {
        replyText =
          'Quishing (QR code phishing) embeds malicious links inside images to bypass email text gateways. Always inspect target URLs before scanning unknown QR codes.';
      } else if (query.includes('password') || query.includes('urgent')) {
        replyText =
          'High-pressure urgency (e.g. "Account suspended in 15 minutes") is a classic social engineering tactic used to bypass critical thinking.';
      }

      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        sender: 'ai',
        text: replyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, aiMsg]);
    }, 600);
  };

  return (
    <>
      {/* Floating Toggle Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-40 flex items-center space-x-2 px-4 py-3 rounded-full bg-gradient-to-r from-cyan-600 to-emerald-600 text-white font-bold text-xs shadow-2xl shadow-cyan-950/60 hover:scale-105 transition-all"
        >
          <Bot className="w-5 h-5" />
          <span>AI Security Assistant</span>
          <Sparkles className="w-3.5 h-3.5 text-amber-300 animate-pulse" />
        </button>
      )}

      {/* Floating Assistant Drawer */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-full max-w-sm rounded-2xl border border-slate-800 bg-slate-900 shadow-2xl overflow-hidden flex flex-col h-[480px]">
          {/* Assistant Header */}
          <div className="p-4 border-b border-slate-800 bg-slate-950/80 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="p-2 rounded-xl bg-cyan-950 border border-cyan-500/30 text-cyan-400">
                <Bot className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-white flex items-center gap-1.5">
                  <span>AI Security Assistant</span>
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                </h4>
                <p className="text-[10px] text-slate-400">
                  {latestScanResult ? `Context Active: ${latestScanResult.id}` : 'Phishing Awareness'}
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Quick Context Action Chip */}
          {latestScanResult && (
            <div className="px-3 py-2 bg-cyan-950/60 border-b border-cyan-500/20 flex items-center justify-between text-[11px]">
              <span className="text-cyan-300 truncate">Latest: {latestScanResult.title}</span>
              <button
                onClick={() => handleSend('Explain my latest scan')}
                className="text-cyan-400 hover:underline font-bold shrink-0 ml-2"
              >
                Explain Scan
              </button>
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 p-4 space-y-3 overflow-y-auto">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex gap-2 text-xs ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {m.sender === 'ai' && (
                  <div className="w-6 h-6 rounded-full bg-cyan-950 border border-cyan-500/30 flex items-center justify-center shrink-0 text-cyan-400">
                    <Bot className="w-3.5 h-3.5" />
                  </div>
                )}
                <div
                  className={`p-3 rounded-2xl max-w-[80%] ${
                    m.sender === 'user'
                      ? 'bg-cyan-600 text-white rounded-br-none'
                      : 'bg-slate-950 border border-slate-800 text-slate-200 rounded-bl-none'
                  }`}
                >
                  <p>{m.text}</p>
                  <span className="text-[9px] opacity-60 block text-right mt-1">{m.timestamp}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Input Footer */}
          <div className="p-3 border-t border-slate-800 bg-slate-950/60 flex items-center space-x-2">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about scan results or phishing..."
              className="flex-1 px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-cyan-500"
            />
            <button
              onClick={() => handleSend()}
              className="p-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold transition-all"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </>
  );
};
