import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
for(const kind of ['hero','about']){
 const bytes=fs.readFileSync(path.join(root,'public/models',`${kind}-workspace.glb`));
 assert.equal(bytes.toString('ascii',0,4),'glTF');assert.equal(bytes.readUInt32LE(8),bytes.length);
 const gltf=JSON.parse(bytes.toString('utf8',20,20+bytes.readUInt32LE(12)));
 assert(gltf.meshes.length>0);assert(gltf.images.length>0);
 if(kind==='about')assert(gltf.animations?.length>0,'About must have an animation');
 for(const image of gltf.images)assert(image.bufferView!==undefined,'Texture must be embedded');
 for(const ext of ['png','webp'])assert(fs.statSync(path.join(root,'public/models',`${kind}-preview.${ext}`)).size>0);
 const blend=fs.readFileSync(path.join(root,'blender',`${kind}-workspace.blend`));assert.equal(blend.toString('ascii',0,7),'BLENDER');
 console.log(`${kind}: GLB valid, ${gltf.meshes.length} meshes, ${gltf.animations?.length??0} animations, packed texture and editable Blender source present`);
}
assert(fs.existsSync(path.join(root,'public/Benish-M-Resume.pdf')));
console.log('Resume and both fallback images are present.');
