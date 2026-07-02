"""
components/voice_input.py
-------------------------
Custom voice input helper for the Predict page.
"""

from __future__ import annotations

import streamlit.components.v1 as components


def render_voice_input() -> None:
    html = """
    <style>
    .voice-shell {
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 22px;
        background: rgba(255,255,255,0.07);
        padding: 18px;
        margin-bottom: 18px;
        color: #ecf8ff;
    }
    .voice-shell h4 {
        margin: 0 0 8px 0;
        font-size: 15px;
        letter-spacing: 0.02em;
    }
    .voice-shell .voice-actions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        align-items: center;
    }
    .voice-shell .voice-button {
        border-radius: 14px;
        border: none;
        background: linear-gradient(135deg, rgba(0,217,192,0.95), rgba(14,122,112,0.95));
        color: white;
        padding: 10px 14px;
        cursor: pointer;
        font-weight: 700;
        transition: transform 120ms ease;
    }
    .voice-shell .voice-button:hover {
        transform: translateY(-1px);
    }
    .voice-shell .voice-note {
        color: rgba(255,255,255,0.72);
        font-size: 12px;
    }
    .voice-shell .voice-bubble {
        margin-top: 12px;
        padding: 14px 16px;
        background: rgba(255,255,255,0.08);
        border-radius: 18px;
        font-size: 13px;
    }
    .voice-shell .voice-hidden {
        display: none;
    }
    </style>
    <div class="voice-shell">
        <h4>Voice & Natural Language Input</h4>
        <div class="voice-actions">
            <button class="voice-button" id="voice-start">🎤 Start Recording</button>
            <button class="voice-button" id="voice-stop">⏹️ Stop</button>
            <div class="voice-note" id="voice-status">Speak naturally: "Area 2500 square feet, three bedrooms, two bathrooms, semi furnished."</div>
        </div>
        <div class="voice-bubble" id="voice-output">Ready to listen.</div>
    </div>
    <script>
    (function() {
        const output = document.getElementById('voice-output');
        const status = document.getElementById('voice-status');
        const startBtn = document.getElementById('voice-start');
        const stopBtn = document.getElementById('voice-stop');
        const SpeechCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;

        if (!SpeechCtor) {
            output.innerText = 'Voice recognition is unavailable in this browser.';
            status.innerText = 'Try a modern browser such as Chrome. Voice entry will still work when supported.';
            startBtn.disabled = true;
            stopBtn.disabled = true;
            return;
        }

        recognition = new SpeechCtor();
        recognition.lang = 'en-IN';
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;
        recognition.continuous = true;

        let finalTranscript = '';
        let isRecording = false;

        const findTargetField = () => {
            const textarea = window.parent.document.querySelector("textarea[placeholder='Speak or type property description']");
            if (textarea) return textarea;
            const all = window.parent.document.querySelectorAll('textarea');
            return Array.from(all).find((el) => el.placeholder && el.placeholder.toLowerCase().includes('speak or type'));
        };

        const updateFormField = (text) => {
            const target = findTargetField();
            if (!target) {
                status.innerText = 'Unable to locate the form field for voice input.';
                return;
            }
            target.value = text;
            target.dispatchEvent(new Event('input', { bubbles: true }));
            target.dispatchEvent(new Event('change', { bubbles: true }));
            status.innerText = 'Voice input inserted into the form. Edit if needed.';
        };

        recognition.onstart = () => {
            output.innerText = 'Listening... speak now.';
            status.innerText = 'Voice recording active.';
            isRecording = true;
        };
        recognition.onresult = (event) => {
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; i += 1) {
                const result = event.results[i];
                if (result.isFinal) {
                    finalTranscript += result[0].transcript + ' ';
                } else {
                    interimTranscript += result[0].transcript + ' ';
                }
            }
            const displayText = (finalTranscript + interimTranscript).trim();
            output.innerText = displayText ? `Detected: "${displayText}"` : 'Listening...';
            if (event.results[event.results.length - 1].isFinal) {
                updateFormField(finalTranscript.trim());
            }
        };
        recognition.onerror = (event) => {
            output.innerText = 'Voice recognition error: ' + event.error;
            status.innerText = 'Please try again or use text input.';
        };
        recognition.onend = () => {
            if (isRecording) {
                status.innerText = 'Continuing to listen for more speech...';
                try {
                    recognition.start();
                } catch (err) {
                    status.innerText = 'Speech recognition stopped. Press Start again to resume.';
                }
            } else {
                status.innerText = 'Recording stopped. Use the text field or press start again.';
            }
        };

        startBtn.addEventListener('click', () => {
            try {
                finalTranscript = '';
                recognition.start();
            } catch (err) {
                status.innerText = 'Unable to start speech recognition.';
            }
        });
        stopBtn.addEventListener('click', () => {
            isRecording = false;
            recognition.stop();
        });
    })();
    </script>
    """
    components.html(html, height=260, scrolling=False)
