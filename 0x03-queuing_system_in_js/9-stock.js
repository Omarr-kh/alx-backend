import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

const getItemById = (id) => {
  if (id < 1 || id > listProducts.length) {
    return null;
  } else {
    return listProducts.filter((product) => product.itemId == id)[0];
  }
};

const app = express();

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

const reserveStockById = (itemId, stock) => {
  client.SET(itemId, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  return await getAsync(itemId);
};

app.get('/list_products/:itemId', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const currStock = getCurrentReservedStockById(itemId);

  if (!currStock) {
    res.json({ status: 'Product not found' });
  } else {
    const product = getItemById(itemId);
    product['currentQuantity'] = stock;
    res.json(product);
  }
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
  } else if (product.initialAvailableQuantity < 1) {
    res.json({ status: 'Not enough stock available', itemId: itemId });
  } else {
    reserveStockById(itemId, product.initialAvailableQuantity);
    res.json({ status: 'Reservation confirmed', itemId: itemId });
  }
});

app.listen(1245)
