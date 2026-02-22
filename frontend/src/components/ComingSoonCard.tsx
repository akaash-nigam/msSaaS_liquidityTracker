"use client";

export default function ComingSoonCard({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-white/5 bg-slate-900/80 backdrop-blur-sm p-6 flex flex-col items-center justify-center text-center min-h-[160px]">
      <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-amber-500/10 text-amber-400 border border-amber-500/20 mb-3">
        Coming Soon
      </span>
      <h3 className="text-sm font-semibold text-white mb-1">{title}</h3>
      <p className="text-xs text-slate-500 max-w-xs">{description}</p>
    </div>
  );
}
