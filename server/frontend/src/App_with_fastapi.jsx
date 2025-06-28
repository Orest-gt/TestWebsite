import { useState } from "react";
import "./static/App4.css";
import { DateTime } from "luxon";

export default function App4() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [show_pass, set_show_pass] = useState(false);

    const sendData = async () => {
        const now = DateTime.now().toLocaleString(DateTime.DATETIME_MED);
        const additional_metadata = "";
        const response = await fetch("http://localhost:8000/api/request_signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password, now, additional_metadata })
        });
        const data_received = await response.json();
        alert(data_received.user_message);
        console.log(data_received.system_message);
    };

    return (
        <div>
            <input 
                type="text" 
                placeholder="Username" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)}
                required></input>
            <br />
            <div style={{ alignItems: "left"}}>
                <label id="password_l"></label>
                <input id="password_l"
                    type={show_pass ? "text" : "password"}
                    placeholder="Password"
                    value={password}
                    onChange={(p) => setPassword(p.target.value)}
                    required
                ></input>
                <button 
                    className="send_password" 
                    onClick={() => set_show_pass(!show_pass)} 
                    disabled={password === ""}
                >   
                {show_pass ? "Hide password" : "Show password"}</button>
                <br />
                <div style={{padding: "10px"}}>
                    <button onClick={sendData}>
                        Save login information
                    </button>
                </div>
                <br />
            </div>
            <br />
        </div>
    );
}