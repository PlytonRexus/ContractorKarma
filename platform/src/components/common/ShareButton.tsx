'use client';

interface ShareButtonProps {
  roadName: string;
  dlpStatus: string;
  contractorName: string | null;
  dlpEndDate: string | null;
  url?: string;
}

export function ShareButton({
  roadName,
  dlpStatus,
  contractorName,
  dlpEndDate,
  url,
}: ShareButtonProps) {
  const handleShare = () => {
    const siteUrl = url || (typeof window !== 'undefined' ? window.location.href : '');
    let message = '';

    if (dlpStatus === 'active' || dlpStatus === 'expiringSoon') {
      message = `Did you know? ${roadName} is UNDER WARRANTY by ${contractorName || 'contractor'} until ${dlpEndDate || 'N/A'}. If the road has defects, the contractor must fix it for free! Check: ${siteUrl}`;
    } else {
      message = `${roadName} - warranty has EXPIRED. The municipality must maintain this road. Check road status and contractor details: ${siteUrl}`;
    }

    const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
  };

  return (
    <button
      onClick={handleShare}
      className="inline-flex items-center gap-2 px-3 py-1.5 text-sm border rounded-lg hover:bg-accent"
    >
      Share on WhatsApp
    </button>
  );
}
