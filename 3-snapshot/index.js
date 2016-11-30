'use strict';

const {ipcMain, app, BrowserWindow} = require('electron');
const path = require('path')

let mainWindow = null;
const port = 10000 + parseInt(Math.random() * 10000)

const server = require('http-server').createServer({
  root: path.join(__dirname, 'viewer/public'),
  cache: -1,
})

server.listen(port, '0.0.0.0', () => {
  console.log(`listening on http://0.0.0.0:${port}`)

  app.on('window-all-closed', function() {
    app.quit();
  });

  app.on('ready', function() {
    mainWindow = new BrowserWindow({
      width: 1200,
      title: 'Snapshotting Assessment Items',
      height: 1000,
    });

    ipcMain.on('minimize', () => {
      mainWindow.minimize();
    });

    ipcMain.on('close', () => {
      mainWindow.close();
    });

    mainWindow.loadURL(`http://0.0.0.0:${port}`);
    mainWindow.webContents.on('did-finish-load', () => {
      const scriptPath = path.join(__dirname, 'src')
      mainWindow.webContents.executeJavaScript(`require("${scriptPath}")`)
    })
    mainWindow.on('closed', function() {
      mainWindow = null;
    });
  });

})
