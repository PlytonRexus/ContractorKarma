import { describe, it, expect } from 'vitest';
import { bbmpContacts, rtiGuidance } from '@/lib/bbmpContacts';

describe('bbmpContacts', () => {
  it('has at least 3 contact entries', () => {
    expect(bbmpContacts.length).toBeGreaterThanOrEqual(3);
  });

  it('has a portal contact', () => {
    const portal = bbmpContacts.find((c) => c.type === 'portal');
    expect(portal).toBeDefined();
    expect(portal!.url).toBeTruthy();
  });

  it('has a phone contact', () => {
    const phone = bbmpContacts.find((c) => c.type === 'phone');
    expect(phone).toBeDefined();
    expect(phone!.phone).toBeTruthy();
  });

  it('has an office contact', () => {
    const office = bbmpContacts.find((c) => c.type === 'office');
    expect(office).toBeDefined();
    expect(office!.address).toBeTruthy();
  });

  it('all contacts have name and description', () => {
    for (const contact of bbmpContacts) {
      expect(contact.name).toBeTruthy();
      expect(contact.description).toBeTruthy();
    }
  });
});

describe('rtiGuidance', () => {
  it('has portal URL', () => {
    expect(rtiGuidance.portalUrl).toBeTruthy();
  });

  it('has fee info', () => {
    expect(rtiGuidance.fee).toContain('10');
  });

  it('has time limits', () => {
    expect(rtiGuidance.timeLimits.responseDeadline).toBeTruthy();
    expect(rtiGuidance.timeLimits.firstAppeal).toBeTruthy();
    expect(rtiGuidance.timeLimits.secondAppeal).toBeTruthy();
  });

  it('has tips', () => {
    expect(rtiGuidance.tips.length).toBeGreaterThan(0);
  });
});
