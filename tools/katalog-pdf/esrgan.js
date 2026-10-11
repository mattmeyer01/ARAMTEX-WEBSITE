// ESRGAN-thick ×4 (UpscalerJS) na WebAssembly: node esrgan.js wej.raw wyj.raw [...]
// Plik raw: szerokość i wysokość (uint32 LE), potem piksele RGB. Uruchamia tools/powieksz_zdjecia.py.
const fs = require('fs'), path = require('path');
const MODS = process.env.MODS;  // katalog node_modules z pakietami (patrz powieksz_zdjecia.py)
const tf = require(path.join(MODS, '@tensorflow/tfjs'));
require(path.join(MODS, '@tensorflow/tfjs-backend-wasm'));
const { getESRGANModelDefinition } = require(path.join(MODS, '@upscalerjs/esrgan-thick/dist/cjs/packages/shared/src/esrgan/esrgan.js'));
const dir = path.join(MODS, '@upscalerjs/esrgan-thick/models/x4');
async function main() {
  await tf.setBackend(process.env.TFB || 'wasm'); await tf.ready();
  const def = getESRGANModelDefinition({ scale: 4, name: 'x', version: '1', meta: { architecture: 'rrdn' } });
  def.setup(tf);
  const mj = JSON.parse(fs.readFileSync(path.join(dir, 'model.json')));
  const bufs = mj.weightsManifest[0].paths.map(p => fs.readFileSync(path.join(dir, p)));
  const all = Buffer.concat(bufs);
  const model = await tf.loadLayersModel({ load: async () => ({
    modelTopology: mj.modelTopology, weightSpecs: mj.weightsManifest[0].weights,
    weightData: all.buffer.slice(all.byteOffset, all.byteOffset + all.byteLength) }) });
  for (let i = 2; i < process.argv.length; i += 2) {
    const raw = fs.readFileSync(process.argv[i]);
    const w = raw.readUInt32LE(0), h = raw.readUInt32LE(4);
    const x = tf.tidy(() => tf.tensor3d(new Uint8Array(raw.buffer, raw.byteOffset + 8, w * h * 3), [h, w, 3], 'int32').toFloat().div(255).expandDims(0));
    const t0 = Date.now();
    const y = model.predict(x);
    const out = await tf.tidy(() => y.squeeze().clipByValue(0, 1).mul(255).round().toInt()).data();
    const buf = Buffer.alloc(8 + out.length); buf.writeUInt32LE(w * 4, 0); buf.writeUInt32LE(h * 4, 4);
    for (let k = 0; k < out.length; k++) buf[8 + k] = out[k];
    fs.writeFileSync(process.argv[i + 1], buf);
    x.dispose(); y.dispose();
    console.log(path.basename(process.argv[i]), w + 'x' + h, ((Date.now() - t0) / 1000).toFixed(1) + 's');
  }
}
main().catch(e => { console.error(e); process.exit(1); });
