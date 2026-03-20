import React, { useState } from "react";

function App() {
  const [slots, setSlots] = useState([]);

  const getSlots = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/free-slots");
      const data = await res.json();
      console.log(data); // 👈 IMPORTANT (check console)
      setSlots(data);
    } catch (error) {
      console.error("Error fetching slots:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Free Slots</h1>

      <button onClick={getSlots}>Get Free Slots</button>

      {slots.length === 0 ? (
        <p>No data yet</p>
      ) : (
        slots.map((dayData, index) => (
          <div key={index} style={{ marginTop: "20px" }}>
            <h2>{dayData.day}</h2>

            {dayData.free_slots.map((slot, i) => (
              <div key={i}>
                ⏰ {slot.start} - {slot.end}
              </div>
            ))}
          </div>
        ))
      )}
    </div>
  );
}

export default App;