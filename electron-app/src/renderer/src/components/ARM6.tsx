import axios from 'axios';
import { stringify } from 'querystring';
import '../assets/ARM6.css'

// Props are reusable pieces
// {} compile things is Javascript
// Este codigo puede sufrir de dividitis
// https://brainstormsandraves.com/web-standards/html-semantics-structure/

const 

function ARM6(){
    
    function Write(){
        // Display python script
    }

    const COP = "0000";
    // COP esta conformado por 4 digitos binarios.

    const DATA = "0000000000000";
    // Data esta conformado por tres digitos hexadecimales de 12 bits.

    {/* Anotaciones:
        - Tener en cuenta cuando se hace operaciones de escritura, verificar si esta activado el Write Buffer */}

    return (
        <>
            <div className="UC">
                <div className="PC">
                      
                </div>
                
                <div className="IR">
                    <h1 className="IRHeader">IR</h1>
                    <div className="InstructionFormat">
                        <div className="COP">{COP}</div>
                        <div className="DATA">{DATA}</div>
                    </div>
                </div>

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