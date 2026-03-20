const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('arcadia', {
  onPlayVideo: (callback) => {
    ipcRenderer.on('play-video', (_event, data) => callback(data));
  },
  onStopVideo: (callback) => {
    ipcRenderer.on('stop-video', (_event) => callback());
  },
});
