import { GoogleSpreadsheet } from "google-spreadsheet";
import { JWT } from 'google-auth-library'
import env from "dotenv";
env.config();

const SCOPES = [
  "https://www.googleapis.com/auth/spreadsheets",
  "https://www.googleapis.com/auth/drive.file",
];

const jwtFromEnv = new JWT({
  email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
  key: process.env.GOOGLE_PRIVATE_KEY,
  scopes: SCOPES,
});

const doc = new GoogleSpreadsheet(
  "1Sh9aNUYvKmPU08oQ9MtBD-GM-dpYBp9AEz-XfwOa7LU", jwtFromEnv
);


await doc.loadInfo(); // loads document properties and worksheets
console.log(doc.title);
