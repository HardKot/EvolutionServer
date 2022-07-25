CREATE TYPE Language as ENUM(
    'AB',
    'AF',
    'AK',
    'SQ',
    'AM',
    'AR',
    'AN',
    'HY',
    'AS',
    'AV',
    'AE',
    'AY',
    'AZ',
    'BA',
    'BM',
    'EU',
    'BE',
    'BN',
    'BH',
    'BI',
    'BO',
    'BS',
    'BR',
    'BG',
    'MY',
    'CA',
    'CS',
    'CH',
    'CE',
    'ZH',
    'CU',
    'CV',
    'KW',
    'CO',
    'CR',
    'CY',
    'DA',
    'DE',
    'DV',
    'NL',
    'DZ',
    'EL',
    'EN',
    'EO',
    'ET',
    'EE',
    'FO',
    'FA',
    'FJ',
    'FI',
    'FR',
    'FY',
    'FF',
    'KA',
    'GD',
    'GA',
    'GL',
    'GV',
    'GN',
    'GU',
    'HT',
    'HA',
    'HE',
    'HZ',
    'HI',
    'HO',
    'HR',
    'HU',
    'IG',
    'IS',
    'IO',
    'II',
    'IU',
    'IE',
    'IA',
    'ID',
    'IK',
    'IT',
    'JV',
    'JA',
    'KL',
    'KN',
    'KS',
    'KR',
    'KK',
    'KM',
    'KI',
    'RW',
    'KY',
    'KV',
    'KG',
    'KO',
    'KJ',
    'KU',
    'LO',
    'LA',
    'LV',
    'LI',
    'LN',
    'LT',
    'LB',
    'LU',
    'LG',
    'MK',
    'MH',
    'ML',
    'MI',
    'MR',
    'MS',
    'MG',
    'MT',
    'MN',
    'NA',
    'NV',
    'NR',
    'ND',
    'NG',
    'NE',
    'NN',
    'NB',
    'NO',
    'NY',
    'OC',
    'OJ',
    'OR',
    'OM',
    'OS',
    'PA',
    'PI',
    'PL',
    'PT',
    'PS',
    'QU',
    'RM',
    'RO',
    'RN',
    'RU',
    'SG',
    'SA',
    'SI',
    'SK',
    'SL',
    'SE',
    'SM',
    'SN',
    'SD',
    'SO',
    'ST',
    'ES',
    'SC',
    'SR',
    'SS',
    'SU',
    'SW',
    'SV',
    'TY',
    'TA',
    'TT',
    'TE',
    'TG',
    'TL',
    'TH',
    'TI',
    'TO',
    'TN',
    'TS',
    'TK',
    'TR',
    'TW',
    'UG',
    'UK',
    'UR',
    'ZU',
    'UZ',
    'VE',
    'VI',
    'VO',
    'WO',
    'XH',
    'WA',
    'YI',
    'YO',
    'ZA'
);

CREATE TYPE TypeMeditation as ENUM(
    'relaxation',
    'breathingPractices',
    'directionalVisualizations',
    'dancePsychotechnics',
    'DMD'
);

CREATE TYPE UserRole as ENUM('USER', 'ADMIN');

CREATE TYPE UserCategory as ENUM('BLOGGER',
'COMMUNITY',
'ORGANIZATION',
'EDITOR',
'WRITER',
'GARDENER',
'FLOWER_MAN',
'PHOTOGRAPHER');

CREATE TYPE UserGender as ENUM('MALE',
'FEMALE',
'OTHER');

