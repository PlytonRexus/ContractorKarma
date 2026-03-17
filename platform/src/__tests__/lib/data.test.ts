import { describe, it, expect } from 'vitest';
import {
  getRoadsForWard,
  getWorksForWard,
  getAllContractors,
  getRedFlags,
  getStats,
  getSearchIndex,
  getRoadById,
  getWorksForRoad,
  getAllWards,
} from '@/lib/data';

describe('data layer', () => {
  it('loads roads for Bellandur ward', () => {
    const roads = getRoadsForWard('bengaluru', 'mahadevapura', '150-bellandur');
    expect(roads.length).toBe(25);
    expect(roads[0].roadId).toBeTruthy();
    expect(roads[0].roadName).toBeTruthy();
  });

  it('loads works for Bellandur ward', () => {
    const works = getWorksForWard('bengaluru', 'mahadevapura', '150-bellandur');
    expect(works.length).toBe(60);
    expect(works[0].jobCode).toBeTruthy();
  });

  it('returns empty array for nonexistent ward', () => {
    const roads = getRoadsForWard('bengaluru', 'mahadevapura', '999-nonexistent');
    expect(roads).toEqual([]);
  });

  it('loads all contractors', () => {
    const contractors = getAllContractors();
    expect(contractors.length).toBe(8);
    expect(contractors[0].contractorId).toBeTruthy();
    expect(contractors[0].legalName).toBeTruthy();
  });

  it('loads red flags', () => {
    const flags = getRedFlags();
    expect(flags.length).toBeGreaterThan(0);
    expect(flags[0].flagId).toBeTruthy();
  });

  it('loads stats', () => {
    const stats = getStats();
    expect(stats).not.toBeNull();
    expect(stats!.totalRoads).toBeGreaterThan(0);
  });

  it('loads search index', () => {
    const index = getSearchIndex();
    expect(index.length).toBeGreaterThan(0);
  });

  it('finds a road by ID', () => {
    const road = getRoadById('blr-mhd-150-001');
    expect(road).not.toBeNull();
    expect(road!.roadName).toBeTruthy();
  });

  it('returns null for nonexistent road ID', () => {
    const road = getRoadById('nonexistent-road');
    expect(road).toBeNull();
  });

  it('gets works for a specific road', () => {
    const works = getWorksForRoad('blr-mhd-150-001');
    expect(works.length).toBeGreaterThan(0);
    works.forEach((w) => expect(w.roadId).toBe('blr-mhd-150-001'));
  });

  it('lists all wards', () => {
    const wards = getAllWards();
    expect(wards.length).toBe(3);
    expect(wards[0].ward.wardName).toBeTruthy();
  });
});
