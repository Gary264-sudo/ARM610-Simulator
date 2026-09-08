import '../assets/MP_Ram.css'
import Palabra from './Palabra'

import axios from 'axios'

function MemoriaPrincipal() {
    // Palabras almacenara el COP, direccion, dato de cada Palabra del form
    const Palabras = new Array(32)

    for(let i = 0; i <= 32; i++){
        Palabras.fill(i, i, i + 1);
    }

    type Word = {
        DireccionByte: number,
        CodigoOperacion: string,
        DireccionDato: number,
    };

    const insertWords = async () => {
        // axios.create sirve de manera de otorgar una configuracion inicial
        // axios.get sirve de manera de obtener datos de un URL
        const res = await axios.get(`http://127.0.0.1:8000/MP_ram/`, { params: {
            // text, input, etc., sera el parametro que sera colocado en el URL
            text: (document.getElementById('text_MP') as HTMLInputElement).value,
        }});
        
        const valueWord = res.data
        
    };

    return (
        <>
            <div className="MemoriaPrincipal_RAM">
                {/* Contiene las direcciones fisicas, donde la data o las instrucciones se almacenan */}
                {/*  */}

                {/* ARM Instruction set */}
                {/* Branch and Branch with Link: B, BL */}
                {/* Single Data transfer: LDR, STR */}
                {/* Arithmetic Operations: ADC, ADD, MUL, SBC, SUB */}
                {/* Logic Operations: AND, EOR, ORR */}
                {/* XOR de manera de obtener el complemento de un numero */}

                <p className="RAMheader">Memoria Principal: RAM</p>
                <div className="RAM">
                    {/* Palabra es la memoria del semiconductor RAM */}
                    {/* La manera en como se obtienen las unidades de información se denomina el modo de acceso*/}
                    {Palabras.map(palabra => 
                        <Palabra key={palabra} palabra={palabra}></Palabra>
                    )}
                    {/* Tiempo de acceso es el lapso transcurrido entre la orden de lectura y la disponibilidad efectiva de la unidad de información buscada */}
                    <p>Tiempo de acceso: </p>
                    <div className="Compiler">
                        <form>
                            <textarea name="text" id="text_MP"></textarea>
                            <input type="submit" onClick={insertWords}/>
                        </form>
                    </div>
                </div>

            </div>
        </>
    )
}

export default MemoriaPrincipal;
