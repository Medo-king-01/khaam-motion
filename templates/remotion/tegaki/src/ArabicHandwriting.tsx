import { TegakiRenderer } from 'tegaki';
import amiri from 'tegaki/fonts/amiri';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';

const SAMPLE_TEXT = 'مرحبا بالعالم';

export const ArabicHandwriting: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = Math.min(frame / Math.max(1, durationInFrames - 1), 1);

  return (
    <AbsoluteFill
      style={{
        alignItems: 'center',
        backgroundColor: '#f5f0e8',
        color: '#202020',
        direction: 'rtl',
        justifyContent: 'center',
        padding: 96,
      }}
    >
      <TegakiRenderer
        font={amiri}
        text={SAMPLE_TEXT}
        direction="rtl"
        time={{ mode: 'controlled', value: progress, unit: 'progress' }}
        style={{
          color: '#202020',
          fontSize: 140,
          lineHeight: 1.5,
          maxWidth: '100%',
          textAlign: 'center',
        }}
      />
    </AbsoluteFill>
  );
};
