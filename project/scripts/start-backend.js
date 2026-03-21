const { spawn } = require("child_process");
const path = require("path");

const backendPath = path.join(__dirname, "../python_backend");

function startBackend() {
  const uvicorn = spawn("uvicorn", ["app:app", "--reload", "--port", "8000"], {
    cwd: backendPath,
    stdio: "inherit",
  });

  uvicorn.on("error", (err) => {
    console.error("Failed to start backend:", err);
    process.exit(1);
  });

  return uvicorn;
}

startBackend();