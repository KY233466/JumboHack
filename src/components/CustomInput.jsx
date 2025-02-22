import React, {forwardRef} from 'react';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import MultipleSelectChip from "./multiSelect";

const CustomInput = forwardRef(({input, setInput, selectedSemesters, setSelectedSemesters, sendMessage}, ref) => {
    return (
        <div className="input-container" ref={ref}>
            <div style={{width: "100%", backgroundColor: "#1c1c1c", borderRadius: "15px"}}>
                <div style={{margin: '10px 10px 0', color: '#a8a8a8'}}>
                    <div>
                        Make it a question! Include both the topic and your intention. "How does pass/fail grading
                        work?"
                        instead of just "pass/fail"
                    </div>
                    <div>Select all semesters that apply *</div>
                </div>
                <MultipleSelectChip selectedSemesters={selectedSemesters}
                                    setSelectedSemesters={setSelectedSemesters}/>
                <div style={{width: "100%", display: "flex", justifyContent: "space-between"}}>
                    <FormControl
                        component="form"
                        sx={{
                            width: '100%',
                            '& .MuiOutlinedInput-notchedOutline': {
                                border: 'none',
                            },
                            '& .MuiOutlinedInput-input': {
                                m: 0,
                                color: 'white',
                                fontSize: '0.8rem',
                                border: "none",
                                width: "calc(100% - 1rem)"
                            },
                            '& .MuiOutlinedInput-root': {
                                padding: '10px 14px',
                                paddingRight: '0'
                            },
                        }}
                        noValidate
                        autoComplete="off"
                    >
                        <TextField
                            value={input}
                            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type a message..."
                            id="outlined-multiline-flexible"
                            multiline
                            maxRows={4}
                        />
                    </FormControl>
                    <button style={{borderRadius: '12px', margin: '10px'}} onClick={sendMessage}>Send</button>
                </div>
            </div>
        </div>
    );
});

export default CustomInput;