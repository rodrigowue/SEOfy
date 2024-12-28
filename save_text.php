<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Recebe os dados enviados pelo cliente
    $data = json_decode(file_get_contents("php://input"));
    $text = $data->text;

    // Exibe o texto capturado (você pode realizar outras operações aqui)
    echo "Texto capturado: " . $text;
} else {
    // Se a requisição não for POST, retorna um erro
    http_response_code(405);
    echo "Método não permitido";
}
?>
