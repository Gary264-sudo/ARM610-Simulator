import '../assets/Palabra.css'

function Palabra(palabra){
    

    return (
        <>
            <div className="PalabraCss">
                <p className="DireccionByte">{palabra.DireccionByte}</p>
                <p className="COP">{palabra.CodigoOperacion}</p>
                <p className="DireccionDato">{palabra.DireccionDato}</p>
            </div>
        </>
    )
}

export default Palabra