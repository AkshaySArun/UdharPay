const BASE=process.env.NEXT_PUBLIC_API_BASE_URL||"http://localhost:8000/api";
export async function api<T=any>(path:string,options:RequestInit={}):Promise<T>{
 const headers=new Headers(options.headers); if(!(options.body instanceof FormData))headers.set("Content-Type","application/json");
 const response=await fetch(`${BASE}${path}`,{...options,headers,credentials:"include"});
 const data=await response.json().catch(()=>({detail:"The server returned an invalid response"}));
 if(!response.ok)throw new Error(data.detail||"Request failed"); return data as T;
}
