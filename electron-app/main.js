const _electron = require('electron');
// En Electron main process devuelve el objeto API; fuera devuelve el path string
const { app, BrowserWindow, ipcMain } = (typeof _electron === 'object' && _electron.app)
  ? _electron
  : require('electron/main') || {};
const path = require('path');
const Redis = require('ioredis');

const isDev = process.env.NODE_ENV === 'development';
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    fullscreen: true,
    frame: false,
    alwaysOnTop: true,
    backgroundColor: '#000000',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      webSecurity: false,
    },
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:3001');
  } else {
    mainWindow.loadFile(path.join(__dirname, 'build', 'index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function resolveVideoPath(relativePath) {
  const absolute = path.isAbsolute(relativePath)
    ? relativePath
    : path.resolve(process.cwd(), '..', relativePath);
  // En Windows file:// necesita triple slash y barras hacia adelante
  return 'file:///' + absolute.replace(/\\/g, '/');
}

function connectRedis() {
  const subscriber = new Redis(REDIS_URL, {
    lazyConnect: false,
    retryStrategy: (times) => Math.min(times * 500, 5000),
  });

  subscriber.on('error', (err) => {
    console.error('[Redis] Connection error:', err.message);
  });

  subscriber.on('connect', () => {
    console.log('[Redis] Connected to', REDIS_URL);
  });

  subscriber.subscribe('arcadiax', (err, count) => {
    if (err) {
      console.error('[Redis] Failed to subscribe:', err.message);
    } else {
      console.log(`[Redis] Subscribed to arcadiax channel (${count} total)`);
    }
  });

  subscriber.on('message', (channel, message) => {
    if (channel !== 'arcadiax') return;

    let parsed;
    try {
      parsed = JSON.parse(message);
    } catch (e) {
      console.error('[Redis] Failed to parse message:', message);
      return;
    }

    const { event, data } = parsed;
    console.log('[Redis] Event received:', event, data);

    if (!mainWindow) return;

    if (event === 'playback.game.play') {
      if (!data.trailer) {
        console.warn('[Electron] Juego sin trailer asignado:', data.nombre);
        return;
      }
      const absolutePath = resolveVideoPath(data.trailer);
      mainWindow.webContents.send('play-video', {
        path: absolutePath,
        title: data.nombre,
        console: data.consola,
        type: 'game',
      });
    } else if (event === 'playback.film.play') {
      const absolutePath = resolveVideoPath(data.ubicacion);
      mainWindow.webContents.send('play-video', {
        path: absolutePath,
        title: data.nombre,
        type: 'film',
      });
    } else if (event === 'playback.stop') {
      mainWindow.webContents.send('stop-video');
    }
  });
}

app.whenReady().then(() => {
  createWindow();
  connectRedis();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
