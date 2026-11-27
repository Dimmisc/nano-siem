// Локальная модель представления. Не является контрактом API команды.
export type Severity = 'critical' | 'high' | 'medium' | 'low';
export type AlertStatus = 'new' | 'ack';
export type AttackType = 'SSH Brute Force' | 'SQL Injection' | 'Web Scan';
export interface Alert { id: string; type: AttackType; ip: string; severity: Severity; count: number; status: AlertStatus; time: string }
export interface DashboardData { totalEvents: number; totalAlerts: number; critical: number; sources: string[]; newAlerts: number; acknowledged: number; timeline: {label:string; count:number}[]; distribution: {type:AttackType; count:number}[]; recent: Alert[] }
export interface DashboardProvider { getDashboard(): Promise<DashboardData> }
export const attackNames: Record<AttackType,string> = {'SSH Brute Force':'Подбор пароля SSH','SQL Injection':'SQL-инъекция','Web Scan':'Сканирование сайта'};
export const severityNames: Record<Severity,string> = {critical:'Критический',high:'Высокий',medium:'Средний',low:'Низкий'};
export const statusNames: Record<AlertStatus,string> = {new:'Новый',ack:'Подтверждён'};
