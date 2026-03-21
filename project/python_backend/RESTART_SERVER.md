# HOW TO RESTART THE API SERVER

## Quick Steps:

1. **Stop the current server** (if running):
   - Press `Ctrl + C` in the terminal where the server is running
   - OR close the terminal window

2. **Navigate to the backend directory**:
   ```
   cd "C:\Users\Ujwal Gowda KR\OneDrive\Desktop\PCB-main\project\python_backend"
   ```

3. **Start the server**:
   ```
   python app.py
   ```
   
   OR if app.py doesn't have a main block:
   ```
   uvicorn app:app --reload --port 8000
   ```

## Detailed Instructions:

### Method 1: Using Python directly
```powershell
cd "C:\Users\Ujwal Gowda KR\OneDrive\Desktop\PCB-main\project\python_backend"
python app.py
```

### Method 2: Using uvicorn directly
```powershell
cd "C:\Users\Ujwal Gowda KR\OneDrive\Desktop\PCB-main\project\python_backend"
uvicorn app:app --reload --port 8000
```

### Method 3: If app.py doesn't start the server automatically
Add this to the end of `app.py`:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Verify Server is Running:

After starting, you should see:
- Server running on `http://localhost:8000`
- API endpoint available at `http://localhost:8000/api/analyze`
- Frontend should connect to `http://localhost:3000`

## Troubleshooting:

- **Port already in use**: Kill the process using port 8000
- **Module not found**: Make sure you're in the correct directory
- **Model not loading**: Check that `quick_trained_model.pth` exists in the directory
