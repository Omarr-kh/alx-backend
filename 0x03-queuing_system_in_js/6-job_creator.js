import kue from 'kue';

const queue = kue.createQueue();
const jobObject = {
  phoneNumber: '01022233351',
  message: 'Message recieved',
};

const job = queue.create('push_notification_code', jobObject).save((err) => {
  if (!err) console.log(`Notification job created: ${job.id}`);
});

job
  .on('complete', () => console.log('Notification job completed'))
  .on('failed', () => console.log('Notification job failed'));
