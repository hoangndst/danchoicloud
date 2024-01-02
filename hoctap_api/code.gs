function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

function getAllGaisImage() {
  var dApp = DriveApp;
  var folder = dApp.getFoldersByName("Học Tập");
  // var gaiFolder = folder.next();
  // var imageFolder = gaiFolder.getFoldersByName("Image");
  var gaiImage = folder.next().getFiles();
  // console.log(gaiImage.hasNext())

  // while (gaiImage.hasNext()) {
  //   Logger.log(gaiImage.next().getId());
  // }
  return gaiImage;
}

function fSheet() {

  var gaiImage = getAllGaisImage();

  var folder = DriveApp.getFoldersByName("GaiAPI").next();
  var files = folder.getFilesByName("Học Tập");
  var sheet = SpreadsheetApp.open(files.next());
  sheet = sheet.getSheetByName("Học Tập");
  var data = [];
  var i = 1;
  while (gaiImage.hasNext()) {
    data.push([i, "https://drive.google.com/uc?id=" + gaiImage.next().getId()]);
    i++;
  }
  // Logger.log(i);
  sheet.getRange("Học Tập!A2:B" + i).setValues(data);
  return true
}

var mock = {
  parameter: {
    sheetNum: "1",
    action: ""
  }
};

function doGet(e) {
  e = e || mock;
  var sheetNum = e.parameter.sheetNum;
  var action = e.parameter.action
  var json = {
    'updated': ''
  }
  if (action === "loadImage") {
    try {
      json.updated = fSheet()
      return ContentService.createTextOutput(JSON.stringify(json)).setMimeType(ContentService.MimeType.JSON);
    } catch (err) {
      json.updated = false
      return ContentService.createTextOutput(JSON.stringify(json)).setMimeType(ContentService.MimeType.JSON);
    }
  }
  json = {
    'image': ''
  };

  var folder = DriveApp.getFoldersByName("GaiAPI").next();
  var files = folder.getFilesByName("Học Tập");
  var sheet = SpreadsheetApp.open(files.next());
  sheet = sheet.getSheetByName("Học Tập");
  var range = sheet.getDataRange();
  var values = range.getValues();
  var id = getRandomInt(2, values.length);
  Logger.log(values.length);
  var done = sheet.getRange("Học Tập!B" + id).getValues();
  json.image = done[0][0];
  Logger.log(json.image);
  return ContentService.createTextOutput(JSON.stringify(json)).setMimeType(ContentService.MimeType.JSON);
}
