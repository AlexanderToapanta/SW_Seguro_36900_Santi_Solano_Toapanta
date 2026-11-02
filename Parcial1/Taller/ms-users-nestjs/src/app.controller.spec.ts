import { AppController } from './app.controller.js';

describe('AppController', () => {
  it('informa el estado y la fecha del servicio', () => {
    const result = new AppController().health();
    expect(result.status).toBe('ok');
    expect(result.service).toBe('user-service');
    expect(Number.isNaN(Date.parse(result.timestamp))).toBe(false);
  });
});
