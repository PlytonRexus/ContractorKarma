export interface OfficialTenure {
  name: string;
  tenureStart: string;
  tenureEnd: string | null;
}

export interface CurrentHolder {
  name: string;
  officialPhone: string | null;
  officialEmail: string | null;
  verifiedDate: string | null;
}

export interface Official {
  officialId: string;
  designation: string;
  currentHolder: CurrentHolder | null;
  history: OfficialTenure[];
  jurisdiction: string;
}
