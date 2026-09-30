import type { BoxDefinition, BoxId } from '../types'

export const BOXES: Record<BoxId, BoxDefinition> = {
  identified: {
    label: 'Records identified',
    defaultText:
      'Records identified from*:\nDatabases (n = )\nRegisters (n = )',
  },
  removed: {
    label: 'Records removed before screening',
    defaultText: 'Records removed before\nscreening:\nDuplicate records removed (n = )\nRecords marked as ineligible by automation tools (n = )\nRecords removed for other reasons (n = )',
  },
  screened: {
    label: 'Records screened',
    defaultText: 'Records screened\n(n = )',
  },
  excluded: {
    label: 'Records excluded',
    defaultText: 'Records excluded**\n(n = )',
  },
  retrieved: {
    label: 'Reports sought for retrieval',
    defaultText: 'Reports sought for retrieval\n(n = )',
  },
  notRetrieved: {
    label: 'Reports not retrieved',
    defaultText: 'Reports not retrieved\n(n = )',
  },
  assessed: {
    label: 'Reports assessed for eligibility',
    defaultText: 'Reports assessed for eligibility\n(n = )',
  },
  excludedReasons: {
    label: 'Reports excluded',
    defaultText:
      'Reports excluded:\nReason 1 (n = )\nReason 2 (n = )\nReason 3 (n = )\netc.',
  },
  included: {
    label: 'Studies included',
    defaultText: 'Studies included in review\n(n = )\nReports of included studies\n(n = )',
  },
}

export const DEFAULT_TEXTS = Object.fromEntries(
  Object.entries(BOXES).map(([id, box]) => [id, box.defaultText]),
) as Record<BoxId, string>
