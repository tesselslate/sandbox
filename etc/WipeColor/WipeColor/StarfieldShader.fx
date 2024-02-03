#define DECLARE_TEXTURE(Name, index) \
    texture Name: register(t##index); \
    sampler Name##Sampler: register(s##index)

#define SAMPLE_TEXTURE(Name, texCoord) tex2D(Name##Sampler, texCoord)

DECLARE_TEXTURE(text, 0);

uniform float4 WipeColor = float4(0, 0, 0, 1);

float4 PS_Starfield(float4 inPos : SV_Position, float4 inColor : COLOR0, float2 uv : TEXCOORD0) : COLOR0 {
    float4 col = SAMPLE_TEXTURE(text, uv);
    if (col.r == 0.0f) {
        return float4(0, 0, 0, 0);
    }

    return WipeColor;
}

technique starfieldshader {
    pass pass0 {
        PixelShader = compile ps_2_0 PS_Starfield();
    }
}