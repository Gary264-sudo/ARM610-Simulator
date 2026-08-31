import AddressBuffer from './components/AddressBuffer'
import JTAGTest from './components/JTAGTest'
import Clock from './components/Clock'

import MMU from './components/MMU'
import Cache from './components/Cache'
import ARM6 from './components/ARM6'

import WriteBuffer from './components/WB'
import COPROC from './components/COPROC'

import ControlRegister from './components/ControlRegister'

import MemoriaPrincipal from './components/MP_Ram'

import './assets/ARM610.css'

function App(): React.JSX.Element {

  return (
    <>
      <div className="ARM610">
        <div className="ARM610_Sup">
          <AddressBuffer></AddressBuffer>
          <JTAGTest></JTAGTest>
          <Clock></Clock>
        </div>

        <div className="ARM610_Mid">
          <MMU></MMU>
          <Cache></Cache>
          <ARM6></ARM6>
        </div>

        <div className="ARM610_Inf">
          <WriteBuffer></WriteBuffer>
        </div>

        <div className="ARM610_Der">
          <ControlRegister></ControlRegister>
          <COPROC></COPROC>
          <MemoriaPrincipal></MemoriaPrincipal>
        </div>
      </div>
    </>
  )
}

export default App
