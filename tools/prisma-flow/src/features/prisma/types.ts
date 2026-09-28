export type PhaseId = 'identification' | 'screening' | 'included'

export type BoxId =
  | 'identified'
  | 'removed'
  | 'screened'
  | 'excluded'
  | 'retrieved'
  | 'notRetrieved'
  | 'assessed'
  | 'excludedReasons'
  | 'included'

export type BoxVariant = 'main' | 'side'

export type ExportQuality = '1x' | '2x' | '3x'

export interface BoxDefinition {
  label: string
  defaultText: string
}

export interface PhaseTheme {
  label: string
  main: string
  side: string
  focus: string
  arrow: string
}

export interface PhaseRow {
  main: BoxId
  side?: BoxId
}

export interface PhaseDefinition {
  id: PhaseId
  label: string
  theme: PhaseTheme
  rows: PhaseRow[]
}
