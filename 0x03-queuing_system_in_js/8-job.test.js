import sinon from 'sinon';
import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();
describe('Testing createPushNotificationsJobs', () => {
  let testSpy;

  before(() => {
    queue.testMode.enter();
  });

  beforeEach(() => {
    testSpy = sinon.spy(console, 'log');
  });

  afterEach(() => {
    queue.testMode.clear();
    testSpy.restore();
  });

  after(() => {
    queue.testMode.exit();
  });

  it('throws an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw(
      Error,
      'Jobs is not an array'
    );
  });

  it('test on a list of jobs (one job) and log the info', () => {
    const jobsData = [
      {
        phoneNumber: '123456789',
        message: 'my message',
      },
    ];

    createPushNotificationsJobs(jobsData, queue);

    expect(testSpy.calledOnceWith(sinon.match('Notification job created: 1')))
      .to.be.true;
    expect(queue.testMode.jobsData.length).to.equal(1);
    expect(queue.testMode.jobsData[0].type).to.equal(
      'push_notification_code_3'
    );
    expect(queue.testMode.jobsData[0].data).to.equal({
      phoneNumber: '123456789',
      message: 'my message',
    });
  });

  it('test on list of 2 jobs', () => {
    const jobsData = [
      {
        phoneNumber: '123456789',
        message: 'my message',
      },
      {
        phoneNumber: '22334455',
        message: 'hello, world',
      },
    ];

    createPushNotificationsJobs(jobsData, queue);

    expect(testSpy.calledOnceWith(sinon.match('Notification job created: 1')))
      .to.be.true;
    expect(queue.testMode.jobsData.length).to.equal(2);
    expect(queue.testMode.jobsData[0].type).to.equal(
      'push_notification_code_3'
    );
    expect(queue.testMode.jobsData[0].data).to.equal({
      phoneNumber: '123456789',
      message: 'my message',
    });
    expect(queue.testMode.jobsData[1].type).to.equal(
      'push_notification_code_3'
    );
    expect(queue.testMode.jobsData[1].data).to.equal({
      phoneNumber: '22334455',
      message: 'hello, world',
    });
  })
});
