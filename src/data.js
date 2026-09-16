export const profile = {
 name: 'Benish M.', email: 'benishm48@gmail.com', location: 'Kanyakumari, India',
 linkedin: 'https://www.linkedin.com/in/benish-m-9a60593b4', github: 'https://github.com/benishm48-create',
 resume: './Benish-M-Resume.pdf',
 skills: [
 {number:'01',title:'Backend & ERP',description:'Business logic that makes everyday work simpler.',items:['Python','Odoo 19','Odoo ORM','FastAPI','REST APIs','QWeb']},
 {number:'02',title:'Frontend',description:'Interfaces that feel clear, responsive and considered.',items:['React','JavaScript','HTML & CSS','Tailwind CSS','Bootstrap','Vite']},
 {number:'03',title:'Data & tools',description:'The tools behind dependable development.',items:['PostgreSQL','SQLAlchemy','Git & GitHub','Docker','Postman','Ubuntu']}
 ],
 projects:[
 {id:'boutique',number:'01',type:'FREELANCE · FULL STACK',title:'Blessings Boutique',description:'From browsing to checkout. A complete online store built for a boutique business.',tags:['React','FastAPI','PostgreSQL'],theme:'boutique',details:'A responsive storefront with product management, checkout, order creation and automatic stock updates. The backend supports admin-protected CRUD operations, email confirmations and WhatsApp notifications.',link:'https://blessings-boutique.onrender.com/',linkLabel:'Visit website'},
 {id:'students',number:'02',type:'ODOO 19 · CUSTOM APPLICATION',title:'Student Management',description:'Students, classes and enrollment. Connected in one organized workspace.',tags:['Python','Odoo ORM','QWeb'],theme:'students',details:'A custom Odoo application connecting students, classes, subjects, departments and teachers. Includes relational models, enrollment workflows, wizards, access controls and downloadable QWeb student reports.'},
 {id:'sales',number:'03',type:'ODOO 19 · ERP CUSTOMIZATION',title:'Sales, made practical.',description:'Tailored product filtering and quotation reports for a smoother sales workflow.',tags:['Python','PostgreSQL','XML'],theme:'sales',details:'Extended Odoo Sales through model and view inheritance. Added Product Make and category-based filtering, customized salesperson and source fields, configured permissions and built quotation PDF reports.'}
 ],
 experience:[
 {date:'JUL 2026 — PRESENT',role:'Python Developer (Odoo) Intern',company:'Banibro Technologies',location:'Nagercoil',description:'Building and customizing Odoo 19 modules, Sales workflows and QWeb reports. Working with PostgreSQL, access controls and application debugging.'},
 {date:'DEC 2025 — MAR 2026',role:'Frontend Development Intern',company:'ALO Info-Tech',location:'Nagercoil',description:'Built responsive interfaces and reusable React components. Collaborated on testing, debugging and version control for real-world web projects.'}
 ]
};
