import { a1y } from "./channel.js";

const optionsQuiz = {
  hour: 19,
  minute: 24,
  chat_id: a1y.chat_id,
  text: "Mai có đi làm không?",
  poll_options: ["Có", "Không"],
  options: {
    is_anonymous: false,
    type: "regular",
    message_thread_id: a1y.topics[0].message_thread_id,
  },
};
