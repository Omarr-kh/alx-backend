import { createClient, print } from 'redis';

const client = createClient()
  .on('error', (err) =>
    console.log(`Redis client not connected to the server: ${err}`)
  )
  .on('connect', () => console.log('Redis client connected to the server'));

const hashObjects = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

for (const [field, value] of Object.entries(hashObjects)) {
  client.hset('HolbertonSchools', field, value, print);
}

client.hgetall('HolbertonSchools', (_err, values) => console.log(values));
