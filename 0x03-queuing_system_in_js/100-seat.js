import express from 'express';
import kue from 'kue';
import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

const reserveSeat = (number) => {
  client.SET('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  return await getAsync('available_seats');
};

reserveSeat(50);
let reservationEnabled = true;

const queue = kue.createQueue();
const app = express();

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    } else {
      return res.json({ status: 'Reservation in process' });
    }
  });

  job
    .on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', (err) =>
      console.log(`Seat reservation job ${job.id} failed: ${err}`)
    );
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const seats = await getCurrentAvailableSeats();
    if (seats === 0) {
      console.log('Error');
      return done(new Error('Not enough seats available'));
    }

    const new_seats = seats - 1;
    reserveSeat(new_seats);
    if (new_seats === 0) {
      reservationEnabled = false;
    }
    return done();
  });

  return res.json({ status: 'Queue processing' });
});

app.listen(1245);
