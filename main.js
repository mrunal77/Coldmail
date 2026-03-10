const { app, BrowserWindow, shell, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess;

function clearEmailAccounts() {
  const accountsFile = path.join(__dirname, 'email_accounts.json');
  if (fs.existsSync(accountsFile)) {
    fs.writeFileSync(accountsFile, '{}');
  }
}

function startFlask() {
  const isDev = !app.isPackaged;
  const pythonScript = isDev 
    ? path.join(__dirname, 'app.py')
    : path.join(process.resourcesPath, 'app.py');
  
  flaskProcess = spawn('python', [pythonScript], {
    cwd: isDev ? __dirname : path.dirname(pythonScript),
    stdio: 'pipe'
  });

  flaskProcess.stdout.on('data', (data) => {
    console.log(`Flask: ${data}`);
  });

  flaskProcess.stderr.on('data', (data) => {
    console.error(`Flask Error: ${data}`);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    backgroundColor: '#0a0a0f',
    show: false
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Wait for Flask to start, then load the app
  setTimeout(() => {
    mainWindow.loadURL('http://localhost:5000');
  }, 3000);

  // Open external links in browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

app.whenReady().then(() => {
  Menu.setApplicationMenu(null);
  clearEmailAccounts();
  startFlask();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
});
