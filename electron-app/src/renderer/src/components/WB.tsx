import '../assets/WB.css'

function WriteBuffer() {
    return (
        <>
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
        </>
    )
}

export default WriteBuffer;