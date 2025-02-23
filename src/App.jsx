import React, { useState, useEffect, useRef } from "react";
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

    // const formattedMessage = `${selectedSemesters.join(", ")}: ${input} `;
    const formattedMessage = input;

    const userMessage = { sender: "You", text: formattedMessage };
    setMessages((prev) => [...prev, userMessage]);
    setTimeout(() => setInput(""), 0);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/advising/query",
        { query: input },
        { timeout: 60000 }
      );
      let finalResponse = response.data.final_response;
      if (!finalResponse || finalResponse.includes("An error occurred")) {
        finalResponse =
          "An error occurred processing your query. Please try again.";
      }
      // Render only one bot message with the final combined response.
      setMessages((prev) => [...prev, { sender: "Bot", text: finalResponse }]);
    } catch (error) {
      console.error("Error processing query:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "Bot", text: "Error processing query. Please try again." },
      ]);
    }
  };

  // Updated sendEmail that renders only the final combined response.
  const sendEmail = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "You", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setTimeout(() => setInput(""), 0);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/advising/batch",
        { email: input },
        { timeout: 60000 }
      );
      let finalResponse = response.data.final_response;
      if (!finalResponse || finalResponse.includes("An error occurred")) {
        finalResponse =
          "An error occurred processing your email. Please try again.";
      }
      // Render only one bot message with the final combined response.
      setMessages((prev) => [...prev, { sender: "Bot", text: finalResponse }]);
    } catch (error) {
      console.error("Error processing email:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "Bot", text: "Error processing email. Please try again." },
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
      <div
        className="chat-box"
        ref={chatBoxRef}
        style={{ height: chatBoxHeight }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === "You" ? "user" : "bot"}`}
          >
            <div>{msg.text}</div>

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
      {/* <div style={{ margin: "10px" }}>
        <button onClick={sendEmail}>Send Email</button>
      </div> */}
    </div>
  );
}

export default Chatbot;
