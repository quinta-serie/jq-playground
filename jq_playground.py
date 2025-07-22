#!/usr/bin/python3

import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtGui import QFont


class JQPlayground(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JQ Playground")
        self.resize(1000, 700)

        # Font padrão
        default_font = QFont("Menlo", 10)

        # Área de JSON (esquerda)
        self.json_input = QTextEdit()
        self.json_input.setPlaceholderText("Insira o JSON aqui...")
        self.json_input.setFont(default_font)

        # Área de comandos JQ (direita)
        self.jq_input = QTextEdit()
        self.jq_input.setPlaceholderText(
            "Insira o comando jq aqui (ex: .foo | .bar)")
        self.jq_input.setFont(default_font)

        # Área de resultado (abaixo)
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setFont(default_font)

        # Botão de execução
        self.run_button = QPushButton("Executar")
        self.run_button.clicked.connect(self.run_jq)
        self.run_button.setStyleSheet(
            """
            font-size: 14px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            """
        )

        # Layouts
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.json_input)
        top_layout.addWidget(self.jq_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(QLabel("Resultado:"))
        main_layout.addWidget(self.result_output)

        self.setLayout(main_layout)

    def run_jq(self):
        json_text = self.json_input.toPlainText()
        jq_command = self.jq_input.toPlainText()

        if not json_text.strip():
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Icon.Critical)
            alert.setText("JSON inválido")
            alert.setInformativeText("Você precisa fornecer um JSON válido.")
            alert.setWindowTitle("Aviso")
            alert.exec()
            return

        if not jq_command.strip():
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Icon.Critical)
            alert.setText("Comando JQ inválido")
            alert.setInformativeText("Você precisa fornecer um comando jq válido.")
            alert.setWindowTitle("Aviso")
            alert.exec()
            return

        try:
            # Usa subprocesso para executar o comando jq com entrada JSON
            result = subprocess.run(
                ["jq", jq_command],
                input=json_text.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if result.returncode == 0:
                self.result_output.setText(result.stdout.decode("utf-8"))
            else:
                self.result_output.setText(
                    "Erro:\n" + result.stderr.decode("utf-8"))

        except Exception as e:
            self.result_output.setText(f"Erro ao executar jq: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JQPlayground()
    window.show()
    sys.exit(app.exec())
