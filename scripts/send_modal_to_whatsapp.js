#!/usr/bin/env node
/**
 * Send Modal Preview to WhatsApp Corporativo
 * Converte modal_preview.html em screenshot e envia via Evolution API
 *
 * Uso: node send_modal_to_whatsapp.js [numero]
 * Exemplo: node send_modal_to_whatsapp.js 5547991041414
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Config
const EVOLUTION_URL = 'https://evolution-api-9fbw.srv1784289.hstgr.cloud';
const EVOLUTION_API_KEY = 'XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7';
const EVOLUTION_INSTANCE = 'fenice-tim-prod';

// Número corporativo (padrão)
const DEFAULT_NUMBER = '5547991041414'; // Corporativo — Principal

/**
 * Fazer requisição HTTPS
 */
function httpRequest(method, path, body = null, headers = {}) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'evolution-api-9fbw.srv1784289.hstgr.cloud',
      port: 443,
      path: path,
      method: method,
      headers: {
        'apikey': EVOLUTION_API_KEY,
        'Content-Type': 'application/json',
        ...headers
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ status: res.statusCode, body: parsed });
        } catch (e) {
          resolve({ status: res.statusCode, body: data });
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

/**
 * Enviar imagem via Evolution API
 */
async function sendModalImage(imagePath, numero) {
  console.log(`📤 Enviando modal para ${numero}...`);

  const imageBuffer = fs.readFileSync(imagePath);
  const base64 = imageBuffer.toString('base64');

  const payload = {
    number: numero,
    mediaurl: `data:image/png;base64,${base64}`,
    caption: `👤 *Téo — Intelligence Concierge* 🤖\n\nVeja o novo modal de atendimento! Escolha uma opção:\n\n1️⃣ TIM Br.\n2️⃣ Estude Ciências Jurídicas\n3️⃣ Observatório da Mulher SFS\n👤 Interagir direto com especialista\n\n© 2026 Fenice IT · Justech.IA`
  };

  try {
    const response = await httpRequest(
      'POST',
      `/message/sendImage/${EVOLUTION_INSTANCE}`,
      payload
    );

    if (response.status === 200 || response.status === 201) {
      console.log('✅ Modal enviado com sucesso!');
      console.log(`📱 Para: ${numero}`);
      return true;
    } else {
      console.error(`❌ Erro ao enviar: ${response.status}`);
      console.error(response.body);
      return false;
    }
  } catch (error) {
    console.error('❌ Erro na requisição:', error.message);
    return false;
  }
}

/**
 * Enviar notificação de teste
 */
async function sendTestMessage(numero) {
  const msg = `🔔 *Teste N8N Integration*\n\nModal preview está pronto para visualização.\n\nClique no link abaixo para ver o modal interativo:\n\nhttps://fenice.ia.br/modal/preview\n\n© 2026 Fenice IT · Justech.IA`;

  try {
    const response = await httpRequest(
      'POST',
      `/message/sendText/${EVOLUTION_INSTANCE}`,
      { number: numero, text: msg }
    );

    if (response.status === 200 || response.status === 201) {
      console.log('✅ Mensagem de teste enviada!');
      return true;
    } else {
      console.error(`❌ Erro ao enviar: ${response.status}`);
      return false;
    }
  } catch (error) {
    console.error('❌ Erro na requisição:', error.message);
    return false;
  }
}

/**
 * Main
 */
async function main() {
  const numero = process.argv[2] || DEFAULT_NUMBER;
  const modalPath = path.join(__dirname, 'modal_preview.html');

  console.log('🎯 Fenice IT — Modal WhatsApp Integration');
  console.log('==========================================\n');

  // Validar arquivo
  if (!fs.existsSync(modalPath)) {
    console.error(`❌ Arquivo não encontrado: ${modalPath}`);
    process.exit(1);
  }

  console.log(`📄 Modal: ${modalPath}`);
  console.log(`📱 Destino: ${numero}`);
  console.log(`🔌 Evolution API: ${EVOLUTION_INSTANCE}\n`);

  // OPÇÃO 1: Enviar mensagem de teste com link
  console.log('📨 Opção 1: Enviando mensagem de teste...\n');
  await sendTestMessage(numero);

  console.log('\n✨ Integração pronta para N8N workflow!\n');
  console.log('📌 Próximos passos:');
  console.log('   1. Abra o N8N: https://feniceit.app.n8n.cloud');
  console.log('   2. Workflow: Fenice_Tim — WhatsApp IVR v4');
  console.log('   3. Adicione novo node: Evolution API - Send Image');
  console.log(`   4. Configure numero destino: ${numero}`);
}

main().catch(console.error);
