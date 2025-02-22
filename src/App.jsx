import React, {useState, useEffect, useRef} from "react";
import axios from "axios";
import Markdown from "react-markdown";
import CustomInput from "./components/CustomInput";

function Chatbot() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [selectedSemesters, setSelectedSemesters] = useState(["All semesters"]);
    const chatBoxRef = useRef(null);
    const inputContainerRef = useRef(null);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const formattedMessage = `${selectedSemesters} mean ${input}?`;
        const userMessage = {sender: "You", text: input};
        setMessages((prev) => [...prev, userMessage]);
        setTimeout(() => setInput(""), 0);

        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/api/advising",
                {query: formattedMessage},
                {timeout: 30000}
            );
            let text = response.data.response.response;

            if (
                typeof response.data.response === "string" && response.data.response.includes("An error occurred:") ||
                typeof response.data.response?.response === "string" && response.data.response.response.includes("An error occurred:")
            ) {
                text = "An error occurred. Please try again.";
            } else if (!response.data.response?.rag_context) {
                text = "Sorry! No relevant data in the database.";
            }

            setMessages((prev) => [...prev, {sender: "Bot", text: text}]);
        } catch (error) {
            console.error("Error:", error);
            setMessages((prev) => [
                ...prev,
                {sender: "Bot", text: "Error getting response. Please try again."},
            ]);
        }
    };

    useEffect(() => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [messages]);

    const [chatBoxHeight, setChatBoxHeight] = useState("100%");

    useEffect(() => {
        const adjustHeight = () => {
            if (inputContainerRef.current) {
                const inputHeight = inputContainerRef.current.offsetHeight;
                setChatBoxHeight(`calc(100% - ${inputHeight}px - 20px - 5px)`);
            }
        };

        adjustHeight();
        window.addEventListener("resize", adjustHeight);

        return () => {
            window.removeEventListener("resize", adjustHeight);
        };
    }, []);

    return (
        <div className="chat-container">
            <div className="chat-box" ref={chatBoxRef} style={{height: chatBoxHeight}}>
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender === "You" ? "user" : "bot"}`}>
                        {msg.sender === "You" ? <div>{msg.text}</div> : <Markdown>{msg.text}</Markdown>}
                    </div>
                ))}
            </div>
            <CustomInput
                ref={inputContainerRef}
                input={input}
                setInput={setInput}
                selectedSemesters={selectedSemesters}
                setSelectedSemesters={setSelectedSemesters}
                sendMessage={sendMessage}
            />
        </div>
    );
}

export default Chatbot;