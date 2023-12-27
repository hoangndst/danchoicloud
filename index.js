import { a1y } from './modules/channel.js';
import { sendMessage } from './modules/bot.js';

const options = {
  chat_id: a1y.chat_id,
  text: 'Dậy học tư tưởng đi @tuda_2',
  message_thread_id: a1y.topics[0].message_thread_id,
};

// catch promise
sendMessage(options, true).catch((error) => {
  console.log(error);
} );
