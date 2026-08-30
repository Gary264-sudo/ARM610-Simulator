import axios from 'axios';
import '../assets/ARM6.css'

import Xarrow from 'react-xarrows';
import SteppedLineTo from 'react-lineto';

// Props are reusable pieces
// {} compile things is Javascript
// Este codigo puede sufrir de dividitis
// https://brainstormsandraves.com/web-standards/html-semantics-structure/



function ARM6(){
    
    function Write(){
        // Display python script
    }

    // PC
    let valuePC = 0x0000;
    let valuePC_hex = valuePC.toString(16)

    const COP = "0000"; // COP esta conformado por 4 digitos binarios.
    const DATA = "0000 0000 0000"; // Data esta conformado por tres digitos hexadecimales de 12 bits.

    // Las funciones de axios pueden ser async, puesto que es una libreria basado en promesas, lo que se alinea con las funciones async
    const changeValuePC = async () => {
        const res = await axios.get("http://127.0.0.1:8000/ARM6_api1/PCvalue/", { params: {
            input: (document.getElementById('input_PC') as HTMLInputElement).value
        }});

        valuePC_hex = res.data;
        document.getElementById('valuePC_hex_JS')!.innerHTML = valuePC_hex;
    };

    {/* Anotaciones:
        - Tener en cuenta cuando se hace operaciones de escritura, verificar si esta activado el Write Buffer */}

    return (
        <>
            <div className="UC">
                <div className="PC">
                    <p className="PCHeader">Program Counter</p>
                    <div className="CounterFormat" id="CF">
                        <div className="valuePC_hex" id="valuePC_hex_JS">{valuePC_hex}</div>
                    </div>
                    <input id="input_PC" type="text"></input>
                    <button id="buttonValuePC" onClick={changeValuePC}>Inserte el valor del PC</button>
                </div>
                
                <div className="IR">
                    <h1 className="IRHeader">IR</h1>
                    <div className="InstructionFormat" id="IF">
                        <div className="COP">{COP}</div>
                        <div className="DATA">{DATA}</div>
                    </div>
                </div>

                <Xarrow start="CF" end="IF" animateDrawing={-3} dashness={true} showTail={true} path="grid"/>

                <div className="Control">
                    <header className="Decodificador">
                        <p>Decodificador</p>
                        <div className=""></div>
                    </header>

                    <section className="UCComponents">
                    </section>
                </div>
            </div>

        </>
    )
}

export default ARM6;