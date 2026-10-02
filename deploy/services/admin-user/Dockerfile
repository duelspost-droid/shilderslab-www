# 원본 Edge 함수를 **코드 수정 없이** 그대로 돌린다.
#   이 파일은 모의해킹 확증 수정을 거친 코드다(0007 관련). 다른 언어로 옮겨 쓰면
#   fail-closed·롤백·"삭제 대상은 DB 가 판정" 같은 성질을 흘릴 위험이 크다.
#   Deno 전용 API 는 Deno.serve 하나뿐이라 공식 이미지에서 그대로 실행된다.
FROM denoland/deno:alpine-2.1.4
WORKDIR /app
# 레포의 함수 원본을 그대로 복사한다(빌드 컨텍스트는 레포 루트 — compose 참조).
COPY supabase/functions/sl-admin-user/index.ts /app/index.ts
USER deno
EXPOSE 8080
# --allow-net 만 준다. 파일·환경 전체 권한은 주지 않는다(--allow-env 는 키 읽기용으로 한정).
CMD ["run", "--allow-net", "--allow-env", "--no-prompt", "/app/index.ts"]
