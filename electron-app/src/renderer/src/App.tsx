import ARM6 from './components/ARM6'

import './assets/ARM610.css'

import Versions from './components/Versions'
import electronLogo from './assets/electron.svg'

function App(): React.JSX.Element {
  const ipcHandle = (): void => window.electron.ipcRenderer.send('ping')

  return (
    <>
      <img alt="logo" className="logo" src={electronLogo} />
      <div className="creator">Powered by electron-vite</div>
      <div className="text">
        Build an Electron app with <span className="react">React</span>
        &nbsp;and <span className="ts">TypeScript</span>
      </div>
      <p className="tip">
        Please try pressing <code>F12</code> to open the devTool
      </p>
      <div className="actions">
        <div className="action">
          <a href="https://electron-vite.org/" target="_blank" rel="noreferrer">
            Documentation
          </a>
        </div>
        <div className="action">
          <a target="_blank" rel="noreferrer" onClick={ipcHandle}>
            Send IPC
          </a>
        </div>
      </div>

      <div className="MMU">
        <p>Memory Management Unit</p>
        {/* El MMU realiza dos funciones primarias:
          - traduce direcciones virtuales a direcciones fisicas
          - controla permisos de acceso de memoria */}
        {/* Las partes de un MMU son: 
          - Translation Look-aside Buffer (TLB)
          - Access control logic
          - Translation table walking logic */}
        
        {/* El MMU soporta accesos de memoria basados en:
          - Secciones: Bloques de memoria comprimidos de 1MB
          - Paginas: Small Pages consiste de bloques de memoria de 4Kb y Large Pages consiste de bloques de memoria de 64Kb */}
        
        {/*  */}

        {/* El Bufferable Bit (B) controla si la operacion de escritura puede o no utilizar el Write Buffer*/}
      </div>

      <div className="4 kByte Cache">
        <p>4 kByte Cache</p>
        {/* <BloqueMemoria></BloqueMemoria> */}
      </div>
      
      <ARM6></ARM6>

      <div className="WB">
        {/* Es aplicado para mejorar el rendimiento del sistema */}
        {/* Almacena ocho palabras de datos y dos direcciones independientes*/}  
        {/* Es activado o desactivado en el bit 3 (W) del Control Register */}
        {/* Las operaciones son activadas o desactivadas en el bit B del MMU, por lo que MMU debe estar "prendido" */}
        {/* En otras palabras, bit W de Control Register y bit B de MMU deben estar activados para escritura del Write Buffer*/}



        {/* Bufferable Write: Escrituras a memoria principal */}
        {/* Si el Write Buffer esta activado y el procesador realiza una escritura a un bufferable area, la data sera colocada en el Write Buffer a velocidades de escritura FLCK mientras que la CPU continua su ejecucion*/}
        {/* Si el Write Buffer esta activado y estuviese lleno (ocho palabras de datos o direcciones llenas), entonces el procesador se detiene hasta que haya suficiente espacio en el buffer */}

        {/* Unbufferable Writes: Escrituras a perifericos I/O */}
        {/* Si el Write Buffer esta desactivado o el CPU realiza una escritura en un unbufferable area, el procesador se estanca hasta que el Write Buffer se vacie y la escritura se complete externamente, lo que puede requerir sincronizacion y varios ciclos de reloj externos. */}

      </div>

      <div className="ControlRegister">
        {/*  */}
      </div>

      <div className="MemoriaPrincipal_RAM">
        {/* Contiene las direcciones fisicas, donde la data o las instrucciones se almacenan */}
        {/*  */}

        {/* ARM Instruction set */}
        {/* Branch and Branch with Link: B, BL */}
        {/* Single Data transfer: LDR, STR */}
        {/* Arithmetic Operations: ADC, ADD, MUL, SBC, SUB */}
        {/* Logic Operations: AND, EOR, ORR */}
      </div>

      <div className="Compiler">
          {/* Fase de desarrollo de la version 3 */}
      </div>

      <Versions></Versions>
    </>
  )
}

export default App
