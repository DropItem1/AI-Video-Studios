import { useEffect, useRef } from "react";

function App() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    let x = 50;
    let y = 50;
    let dx = 2;
    let dy = 2;

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.beginPath();
      ctx.arc(x, y, 20, 0, Math.PI * 2);
      ctx.fillStyle = "blue";
      ctx.fill();
      ctx.closePath();

      x += dx;
      y += dy;

      if (x + 20 > canvas.width || x - 20 < 0) dx = -dx;
      if (y + 20 > canvas.height || y - 20 < 0) dy = -dy;

      requestAnimationFrame(draw);
    }

    draw();
  }, []);

  return (
    <div style={{ textAlign: "center" }}>
      <h1>🎨 My Animation App</h1>
      <canvas ref={canvasRef} width={500} height={500} style={{ border: "1px solid black" }} />
    </div>
  );
}

export default App;
