import type {DashboardData, DashboardProvider} from './model';
// Значения карточек и последние три предупреждения — из макета Figma.
// Ряд графика восстановлен приблизительно по изображению, сумма = 124.
export const demo: DashboardData = {
 totalEvents:124,totalAlerts:6,critical:2,sources:['Nginx','SSH'],newAlerts:4,acknowledged:2,
 timeline:[{label:'−24 ч',count:12},{label:'−20 ч',count:18},{label:'−16 ч',count:14},{label:'−12 ч',count:17},{label:'−8 ч',count:29},{label:'Сейчас',count:34}],
 distribution:[{type:'SSH Brute Force',count:3},{type:'SQL Injection',count:2},{type:'Web Scan',count:1}],
 recent:[
 {id:'ALT-0248',type:'SQL Injection',ip:'192.0.2.40',severity:'critical',count:3,status:'new',time:'14:52:10'},
 {id:'ALT-0247',type:'SSH Brute Force',ip:'203.0.113.7',severity:'high',count:15,status:'new',time:'14:48:02'},
 {id:'ALT-0246',type:'SQL Injection',ip:'192.0.2.41',severity:'critical',count:2,status:'ack',time:'14:42:19'}]
};
export const demoProvider: DashboardProvider = {async getDashboard(){return structuredClone(demo)}};
