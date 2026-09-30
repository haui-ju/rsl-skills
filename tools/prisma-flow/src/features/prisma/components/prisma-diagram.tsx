import { Fragment } from 'react'
import type { Ref } from 'react'

import { PHASES } from '../constants/phases'
import type { PhaseDefinition } from '../types'
import { FlowArrow } from './flow-arrow'
import { PhaseLabel } from './phase-label'
import { PrismaBox } from './prisma-box'

interface PrismaDiagramProps {
  ref?: Ref<HTMLDivElement>
}

export function PrismaDiagram({ ref }: PrismaDiagramProps) {
  return (
    <div ref={ref} className="group/diagram flex flex-col bg-white p-12">
      <div className="mb-4 flex gap-4">
        <div className="w-10 shrink-0" />
        <div className="flex w-[688px] items-center justify-center rounded-md border-[1.5px] border-black bg-[#ffc000] py-2">
          <span className="text-[15px] font-semibold text-black">
            Identification of studies via databases and registers
          </span>
        </div>
      </div>
      {PHASES.map((phase, index) => (
        <Fragment key={phase.id}>
          {index > 0 && (
            <FlowArrow direction="down" className="ml-14 text-black" />
          )}
          <PhaseSection phase={phase} />
        </Fragment>
      ))}
    </div>
  )
}

function PhaseSection({ phase }: { phase: PhaseDefinition }) {
  const { theme } = phase

  return (
    <section className="flex gap-4">
      <PhaseLabel label={phase.label} theme={theme} />
      <div className="flex flex-col">
        {phase.rows.map((row, index) => (
          <Fragment key={row.main}>
            {index > 0 && (
              <FlowArrow direction="down" className={theme.arrow} />
            )}
            <div className="flex items-stretch">
              <PrismaBox id={row.main} variant="main" theme={theme} />
              {row.side && (
                <>
                  <FlowArrow direction="right" className={theme.arrow} />
                  <PrismaBox id={row.side} variant="side" theme={theme} />
                </>
              )}
            </div>
          </Fragment>
        ))}
      </div>
    </section>
  )
}
