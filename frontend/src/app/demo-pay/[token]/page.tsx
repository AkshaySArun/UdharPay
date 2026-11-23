"use client";

import { useEffect, useState, type CSSProperties } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft, Check, ChevronRight, CreditCard, Info, LockKeyhole, Store, Wallet, X } from "lucide-react";
import { api } from "@/services/api";

type DemoRequest = { order_id: string; amount: string; status: string; shop_name: string; demo: boolean };
type Method = "upi" | "card" | "netbanking";

const money = (value: string) => new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", minimumFractionDigits: 2 }).format(Number(value));

export default function DemoPayPage() {
  const { token } = useParams<{ token: string }>();
  const [request, setRequest] = useState<DemoRequest | null>(null);
  const [error, setError] = useState("");
  const [method, setMethod] = useState<Method>("upi");
  const [result, setResult] = useState<"success" | "failed" | null>(null);

  useEffect(() => {
    api<DemoRequest>(`/payments/demo-link/${encodeURIComponent(token)}`).then(setRequest).catch((e: Error) => setError(e.message));
  }, [token]);

  const simulate = (status: "success" | "failed") => setResult(status);

  return (
    <main style={{ minHeight: "100vh", background: "#f2f4f7", padding: "28px 16px", color: "#17191d", fontFamily: "Arial, sans-serif" }}>
      <div style={{ width: "min(980px, 100%)", margin: "0 auto" }}>
        <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 9, fontWeight: 750, fontSize: 18 }}><div style={{ background: "#176bff", color: "white", borderRadius: 8, width: 32, height: 32, display: "grid", placeItems: "center" }}><Wallet size={18}/></div>Payment checkout</div>
          <div style={{ display: "flex", gap: 6, alignItems: "center", color: "#647084", fontSize: 12 }}><LockKeyhole size={14}/> Secure demo</div>
        </header>

        {error ? <section style={panel}><h1 style={{ fontSize: 22 }}>Payment request unavailable</h1><p style={{ color: "#667085", lineHeight: 1.6 }}>{error}</p></section> : !request ? <section style={panel}>Loading checkout…</section> : result ? (
          <section style={{ ...panel, maxWidth: 520, margin: "48px auto", textAlign: "center", padding: 36 }}>
            <div style={{ width: 58, height: 58, borderRadius: "50%", margin: "0 auto 16px", display: "grid", placeItems: "center", background: result === "success" ? "#e7f7ed" : "#fff0ef", color: result === "success" ? "#168342" : "#c9362b" }}>{result === "success" ? <Check size={27}/> : <X size={27}/>}</div>
            <div style={{ color: "#7b8494", fontSize: 11, fontWeight: 700, letterSpacing: 1.1 }}>SIMULATED CHECKOUT RESULT</div>
            <h1 style={{ fontSize: 24, margin: "10px 0" }}>{result === "success" ? "Demo payment successful" : "Demo payment failed"}</h1>
            <p style={{ color: "#667085", lineHeight: 1.6, margin: "0 auto 20px", maxWidth: 380 }}>{result === "success" ? "The checkout flow was previewed. No payment was made and the merchant balance was not changed." : "This is a simulated failure. No payment was attempted and the merchant balance was not changed."}</p>
            <button onClick={() => setResult(null)} style={primaryButton}><ArrowLeft size={16}/> Back to checkout</button>
          </section>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1.45fr) minmax(270px, .8fr)", gap: 18, alignItems: "start" }}>
            <section style={panel}>
              <div style={{ background: "#fff7e6", color: "#815d12", border: "1px solid #f0dfb6", padding: "11px 13px", borderRadius: 9, display: "flex", gap: 9, fontSize: 12, lineHeight: 1.5, marginBottom: 21 }}><Info size={16} style={{ flexShrink: 0, marginTop: 1 }}/><span><b>Demo interface only.</b> This is a local checkout preview, not Cashfree. It never collects payment details or processes money.</span></div>
              <div style={{ fontSize: 12, color: "#758094", marginBottom: 7 }}>Choose a payment method</div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 9, marginBottom: 20 }}>
                {([["upi", "UPI", <Wallet size={17}/>], ["card", "Cards", <CreditCard size={17}/>], ["netbanking", "Net banking", <Store size={17}/>]] as const).map(([id, label, icon]) => <button key={id} onClick={() => setMethod(id)} style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, border: method === id ? "1px solid #176bff" : "1px solid #e1e5eb", background: method === id ? "#f0f5ff" : "white", color: method === id ? "#1459d9" : "#465064", borderRadius: 9, padding: "12px 7px", fontSize: 12, fontWeight: 650, cursor: "pointer" }}>{icon}{label}</button>)}
              </div>
              <div style={{ border: "1px solid #e7eaf0", borderRadius: 10, padding: 16, minHeight: 126 }}>
                {method === "upi" ? <><b style={{ fontSize: 14 }}>UPI</b><p style={{ color: "#778094", fontSize: 12, lineHeight: 1.5, margin: "7px 0 0" }}>Preview the UPI payment step. In a real sandbox checkout, Cashfree would show the available UPI options here.</p></> : method === "card" ? <><b style={{ fontSize: 14 }}>Credit or debit card</b><p style={{ color: "#778094", fontSize: 12, lineHeight: 1.5, margin: "7px 0 0" }}>Card form preview. Do not enter real card details into this demo.</p></> : <><b style={{ fontSize: 14 }}>Net banking</b><p style={{ color: "#778094", fontSize: 12, lineHeight: 1.5, margin: "7px 0 0" }}>Bank selection preview. No bank connection is made in the demo.</p></>}
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 9, marginTop: 18 }}>
                <button onClick={() => simulate("success")} style={primaryButton}>Simulate successful payment <ChevronRight size={16}/></button>
                <button onClick={() => simulate("failed")} style={secondaryButton}>Simulate failure</button>
              </div>
              <p style={{ fontSize: 11, color: "#8a93a2", margin: "15px 0 0", lineHeight: 1.5 }}>Buttons only preview success and failure screens. They do not change the payment record or khata balance.</p>
            </section>

            <aside style={{ ...panel, padding: 0, overflow: "hidden" }}>
              <div style={{ background: "#f8f9fb", borderBottom: "1px solid #edf0f3", padding: "16px 18px", fontSize: 13, fontWeight: 700 }}>Order summary</div>
              <div style={{ padding: 18 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}><div style={{ width: 36, height: 36, borderRadius: 9, background: "#eaf4ee", color: "#177552", display: "grid", placeItems: "center" }}><Store size={17}/></div><div><div style={{ fontSize: 13, fontWeight: 700 }}>{request.shop_name}</div><div style={{ fontSize: 11, color: "#87909e", marginTop: 3 }}>Merchant</div></div></div>
                <div style={{ borderTop: "1px solid #edf0f3", paddingTop: 16, display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 13, color: "#606a79" }}><span>Amount due</span><strong style={{ color: "#17191d", fontSize: 20 }}>{money(request.amount)}</strong></div>
                <div style={{ marginTop: 15, fontSize: 10, color: "#9199a5", wordBreak: "break-all" }}>Demo order · {request.order_id}</div>
              </div>
            </aside>
          </div>
        )}
        <footer style={{ textAlign: "center", color: "#8d95a1", fontSize: 11, marginTop: 18 }}>Demo payment screen · no real money or payment data involved</footer>
      </div>
    </main>
  );
}

const panel: CSSProperties = { background: "white", border: "1px solid #e7eaf0", borderRadius: 13, padding: 20, boxShadow: "0 4px 18px rgba(20,30,50,.035)" };
const primaryButton: CSSProperties = { display: "inline-flex", alignItems: "center", justifyContent: "center", gap: 8, background: "#176bff", color: "white", border: 0, borderRadius: 8, padding: "12px 15px", fontSize: 12, fontWeight: 700, cursor: "pointer" };
const secondaryButton: CSSProperties = { display: "inline-flex", alignItems: "center", justifyContent: "center", gap: 8, background: "white", color: "#344054", border: "1px solid #d8dde6", borderRadius: 8, padding: "11px 15px", fontSize: 12, fontWeight: 700, cursor: "pointer" };
