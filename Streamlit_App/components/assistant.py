"""
components/assistant.py
-----------------------
Floating AI assistant widget rendered as a custom HTML component.
"""

from __future__ import annotations

import streamlit.components.v1 as components


def render_ai_assistant() -> None:
    html = """
    <style>
    #ai-assistant-shell {
        position: fixed;
        right: 22px;
        bottom: 18px;
        width: 340px;
        max-width: calc(100vw - 32px);
        z-index: 9999;
        font-family: 'Inter', sans-serif;
    }
    #ai-assistant-shell .ai-button {
        width: 100%;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.16);
        background: linear-gradient(135deg, rgba(0, 217, 192, 0.95), rgba(9, 105, 121, 0.95));
        color: #fff;
        font-weight: 700;
        padding: 14px 16px;
        cursor: pointer;
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.18);
    }
    #ai-assistant-shell .ai-panel {
        margin-top: 12px;
        border-radius: 28px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(18px);
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.16);
        background: rgba(8, 17, 30, 0.95);
        color: #e8eef9;
    }
    #ai-assistant-shell .ai-panel.hidden { display: none; }
    #ai-assistant-shell .ai-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        padding: 18px 18px 14px 18px;
        background: rgba(255, 255, 255, 0.05);
    }
    #ai-assistant-shell .ai-header h4 {
        margin: 0;
        font-size: 14px;
    }
    #ai-assistant-shell .ai-header small {
        color: rgba(255,255,255,0.65);
    }
    #ai-assistant-shell .ai-messages {
        padding: 0 18px 12px 18px;
        max-height: 300px;
        overflow-y: auto;
        display: grid;
        gap: 10px;
    }
    .ai-message {
        display: inline-flex;
        gap: 10px;
        align-items: flex-start;
        max-width: 100%;
    }
    .ai-message.user .ai-bubble {
        background: rgba(203, 240, 238, 0.18);
        color: #eef4f9;
        margin-left: auto;
        border-radius: 18px 18px 12px 18px;
    }
    .ai-message.assistant .ai-bubble {
        background: rgba(255,255,255,0.08);
        color: #f8fbff;
        border-radius: 18px 18px 18px 12px;
    }
    .ai-message .ai-bubble {
        padding: 12px 14px;
        line-height: 1.5;
        font-size: 13px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.16);
    }
    .ai-footer {
        padding: 0 18px 18px 18px;
        display: grid;
        gap: 10px;
    }
    .ai-footer textarea {
        width: 100%;
        min-height: 68px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.06);
        color: #fff;
        padding: 12px 14px;
        resize: vertical;
        font-size: 13px;
    }
    .ai-footer button {
        border-radius: 14px;
        border: none;
        padding: 11px 14px;
        cursor: pointer;
        font-weight: 700;
    }
    .ai-footer .send-btn {
        background: linear-gradient(135deg, #00d9c0, #0f766e);
        color: #fff;
    }
    .ai-footer .mic-btn {
        background: rgba(255,255,255,0.08);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.14);
    }
    .ai-footer .mic-btn.disabled {
        opacity: 0.45;
        cursor: not-allowed;
    }
    .ai-avatar {
        width: 56px;
        height: 56px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(0,217,192,0.95), rgba(9,105,121,0.95));
        display: inline-flex;
        position: relative;
        align-items: center;
        justify-content: center;
        box-shadow: 0 12px 22px rgba(0, 0, 0, 0.22);
    }
    .ai-avatar::before {
        content: '';
        position: absolute;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: rgba(255,255,255,0.35);
        top: 10px;
        left: 12px;
        box-shadow: 24px 0 0 rgba(255,255,255,0.35);
    }
    .ai-avatar .face {
        position: relative;
        width: 100%;
        height: 100%;
    }
    .ai-avatar .eye {
        position: absolute;
        top: 20px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #fff;
        animation: assistant-blink 4000ms infinite;
    }
    .ai-avatar .eye.left { left: 14px; }
    .ai-avatar .eye.right { right: 14px; }
    .ai-avatar .mouth {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        bottom: 14px;
        width: 18px;
        height: 6px;
        border-radius: 999px;
        background: rgba(255,255,255,0.9);
    }
    .ai-command-hint {
        margin-top: 10px;
        padding: 10px 12px;
        border-radius: 16px;
        background: rgba(0,217,192,0.12);
        border: 1px solid rgba(0,217,192,0.18);
        color: #d8ffff;
        font-size: 12px;
        line-height: 1.4;
    }
    @keyframes assistant-bob {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-2px); }
    }
    @keyframes assistant-blink {
        0%, 93%, 100% { transform: scaleY(1); }
        95%, 98% { transform: scaleY(0.1); }
    }
    .ai-note {
        padding: 0 18px 12px 18px;
        font-size: 12px;
        color: rgba(255,255,255,0.68);
    }
    </style>
    <div id="ai-assistant-shell">
        <button class="ai-button" id="assistant-toggle">AI Assistant</button>
        <div class="ai-panel hidden" id="assistant-panel">
            <div class="ai-header" style="align-items: center;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div class="ai-avatar">
                        <div class="face">
                            <div class="eye left"></div>
                            <div class="eye right"></div>
                            <div class="mouth"></div>
                        </div>
                    </div>
                    <div>
                        <strong>Estimate Assistant</strong>
                        <div style="font-size:11px; color:rgba(255,255,255,0.6); margin-top:4px;">Ask for help, definitions, or page actions.</div>
                    </div>
                </div>
                <button id="assistant-close" style="background:none;border:none;color:#fff;font-size:18px;cursor:pointer;">×</button>
            </div>
            <div class="ai-messages" id="assistant-messages">
                <div class="ai-message assistant"><div class="ai-bubble">Hi! I can explain this platform, the inputs, and where to go. Try asking "What does Area mean?" or "Navigate to Analytics."</div></div>
            </div>
            <div class="ai-footer">
                <textarea id="assistant-input" placeholder="Type your question or press the mic..."></textarea>
                <div style="display:flex; gap:10px;">
                    <button class="mic-btn" id="assistant-mic" type="button">🎙️ Voice</button>
                    <button class="send-btn" id="assistant-send" type="button">Send</button>
                </div>
            </div>
            <div class="ai-command-hint">Try: “Navigate to Analytics”, “Fill form from voice”, or “What does area mean?”.</div>
            <div class="ai-note" id="assistant-note"></div>
        </div>
    </div>
    <script>
    (function() {
        const toggle = document.getElementById('assistant-toggle');
        const panel = document.getElementById('assistant-panel');
        const close = document.getElementById('assistant-close');
        const send = document.getElementById('assistant-send');
        const mic = document.getElementById('assistant-mic');
        const input = document.getElementById('assistant-input');
        const messages = document.getElementById('assistant-messages');
        const note = document.getElementById('assistant-note');
        let recognition;
        let micEnabled = false;

        function appendMessage(role, text) {
            const wrapper = document.createElement('div');
            wrapper.className = 'ai-message ' + role;
            const bubble = document.createElement('div');
            bubble.className = 'ai-bubble';
            bubble.innerText = text;
            wrapper.appendChild(bubble);
            messages.appendChild(wrapper);
            messages.scrollTop = messages.scrollHeight;
        }

        const pages = {
            dashboard: 'app.py',
            predict: 'pages/1_Predict.py',
            analytics: 'pages/2_Analytics.py',
            reports: 'pages/3_Reports.py',
            history: 'pages/4_History.py',
            settings: 'pages/5_Settings.py',
            about: 'pages/6_About.py',
            model: 'pages/7_Model_Info.py',
            architecture: 'pages/8_Architecture.py',
        };

        function navigateTo(page) {
            if (!page) return false;
            window.parent.location.search = '?page=' + encodeURIComponent(page);
            return true;
        }

        function respondTo(text) {
            const normalized = text.toLowerCase();
            let reply = 'I can help with the platform, forms, and navigation. Try asking for definitions or how to use the app.';

            if (/what.*project|what.*this project/.test(normalized)) {
                reply = 'This platform is a polished AI real estate tool for estimating house prices and exploring dataset analytics using a persisted ML model.';
            } else if (/how.*use|how.*use it/.test(normalized)) {
                reply = 'Use Predict to enter property details, Analytics to explore the dataset, Reports to export results, and History to review past estimates.';
            } else if (/what.*area/.test(normalized)) {
                reply = 'Area means the built-up property size in square feet, which is one of the most important factors used by the model.';
            } else if (/what.*furnishing.*status/.test(normalized)) {
                reply = 'Furnishing Status indicates whether the home is Furnished, Semi Furnished, or Unfurnished.';
            } else if (/what.*model|which.*model/.test(normalized)) {
                reply = 'The app loads a persisted regression model from the training pipeline. The exact algorithm is stored in the model artifact.';
            } else if (/explain.*prediction/.test(normalized)) {
                reply = 'The prediction is an estimated market value produced by the ML model based on your entered property features. It is an approximation, not a formal valuation.';
            } else if (/reset.*form/.test(normalized)) {
                reply = 'You can reset the form on the Predict page using the Reset button, or refresh the page to clear all inputs.';
            } else if (/(navigate|go to|open).*analytics/.test(normalized)) {
                reply = 'Opening Analytics now.';
                navigateTo(pages.analytics);
            } else if (/(navigate|go to|open).*reports/.test(normalized)) {
                reply = 'Opening Reports now.';
                navigateTo(pages.reports);
            } else if (/(navigate|go to|open).*history/.test(normalized)) {
                reply = 'Opening History now.';
                navigateTo(pages.history);
            } else if (/(navigate|go to|open).*settings/.test(normalized)) {
                reply = 'Opening Settings now.';
                navigateTo(pages.settings);
            } else if (/(navigate|go to|open).*about/.test(normalized)) {
                reply = 'Opening About now.';
                navigateTo(pages.about);
            } else if (/(navigate|go to|open).*model/.test(normalized)) {
                reply = 'Opening Model Info now.';
                navigateTo(pages.model);
            } else if (/(navigate|go to|open).*architecture/.test(normalized)) {
                reply = 'Opening Architecture now.';
                navigateTo(pages.architecture);
            } else if (/(navigate|go to|open).*predict/.test(normalized)) {
                reply = 'Opening Predict now.';
                navigateTo(pages.predict);
            } else if (/(navigate|go to|open).*dashboard/.test(normalized)) {
                reply = 'Opening Dashboard now.';
                navigateTo(pages.dashboard);
            }

            appendMessage('assistant', reply);
            note.innerText = '';
        }

        function handleSend() {
            const value = input.value.trim();
            if (!value) {
                note.innerText = 'Enter a question or use the microphone if available.';
                return;
            }
            appendMessage('user', value);
            input.value = '';
            respondTo(value);
        }

        toggle.addEventListener('click', function() {
            panel.classList.toggle('hidden');
        });
        close.addEventListener('click', function() {
            panel.classList.add('hidden');
        });
        send.addEventListener('click', handleSend);
        input.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                handleSend();
            }
        });

        const SpeechCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechCtor) {
            mic.classList.add('disabled');
            note.innerText = 'Voice input unavailable in this browser.';
        } else {
            recognition = new SpeechCtor();
            recognition.lang = 'en-IN';
            recognition.interimResults = true;
            recognition.maxAlternatives = 1;
            recognition.continuous = true;

            let finalTranscript = '';
            let isListening = false;

            const findPredictionField = () => {
                const textarea = window.parent.document.querySelector("textarea[placeholder='Speak or type property description']");
                if (textarea) return textarea;
                const all = window.parent.document.querySelectorAll('textarea');
                return Array.from(all).find((el) => el.placeholder && el.placeholder.toLowerCase().includes('speak or type'));
            };

            const shouldAutoFillPrediction = (text) => {
                const keywords = ['area', 'bedroom', 'bathroom', 'stories', 'parking', 'main road', 'guest room', 'basement', 'hot water', 'air conditioning', 'preferred area', 'furnished'];
                return keywords.some((keyword) => text.toLowerCase().includes(keyword));
            };

            const updatePredictionField = (text) => {
                const predictionField = findPredictionField();
                if (!predictionField) return false;
                predictionField.value = text;
                predictionField.dispatchEvent(new Event('input', { bubbles: true }));
                predictionField.dispatchEvent(new Event('change', { bubbles: true }));
                return true;
            };

            recognition.onresult = function(event) {
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i += 1) {
                    const result = event.results[i];
                    if (result.isFinal) {
                        finalTranscript += result[0].transcript + ' ';
                    } else {
                        interimTranscript += result[0].transcript + ' ';
                    }
                }
                const transcript = (finalTranscript + interimTranscript).trim();
                input.value = transcript;
                const isFinal = event.results[event.results.length - 1].isFinal;
                note.innerText = isFinal ? 'Recognized speech. Press Send to ask the assistant.' : 'Listening... keep speaking.';
                if (isFinal && shouldAutoFillPrediction(transcript)) {
                    if (updatePredictionField(transcript)) {
                        note.innerText = 'Property details detected and auto-filled in the prediction form.';
                    }
                }
            };
            recognition.onerror = function(event) {
                note.innerText = 'Voice recognition failed: ' + event.error;
            };
            recognition.onend = function() {
                if (isListening) {
                    try {
                        recognition.start();
                        note.innerText = 'Continuing to listen...';
                    } catch (error) {
                        isListening = false;
                        note.innerText = 'Voice recognition stopped. Tap mic again to restart.';
                    }
                } else {
                    note.innerText = 'Recording stopped.';
                }
            };
            mic.addEventListener('click', function() {
                if (mic.classList.contains('disabled')) return;
                try {
                    isListening = true;
                    finalTranscript = input.value.trim() ? input.value.trim() + ' ' : '';
                    recognition.start();
                    note.innerText = 'Listening... speak naturally now.';
                } catch (error) {
                    note.innerText = 'Unable to start voice recognition.';
                }
            });
        }
    })();
    </script>
    """
    components.html(html, height=520, scrolling=False)
